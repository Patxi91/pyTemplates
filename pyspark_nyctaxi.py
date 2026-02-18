# Databricks notebook source
# COMMAND ----------
# CELL 1 - Setup imports and display helper
# Run first. It prepares Spark helpers and a display/show fallback.
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql import SparkSession


# Databricks provides `spark`; local execution uses SparkSession fallback.
spark = globals().get("spark") or SparkSession.builder.getOrCreate()
dbutils = globals().get("dbutils")


def show_df(df, n=20, title=None):
	"""
	Try Databricks display() first (nice table/chart UI),
	and fall back to .show() for non-Databricks execution.
	"""
	if title:
		print(f"\n=== {title} ===")
	display_fn = globals().get("display")
	if callable(display_fn):
		display_fn(df.limit(n))
	else:
		df.show(n, truncate=False)


# COMMAND ----------
# CELL 2 - Read the source dataset
# Loads the Databricks sample taxi table into a DataFrame.
table_name = "samples.nyctaxi.trips"
trips_raw = spark.table(table_name)

print(f"Loaded table: {table_name}")
print(f"Row count: {trips_raw.count():,}")


# COMMAND ----------
# CELL 3 - Quick data understanding
# Prints schema and first rows so you verify column names/types.
trips_raw.printSchema()
show_df(trips_raw, n=20, title="Raw sample records")


# COMMAND ----------
# CELL 4 - Keep relevant columns and parse timestamps
# Creates a narrower DataFrame and converts datetime strings to timestamp type.
trips = (
	trips_raw.select(
		"tpep_pickup_datetime",
		"tpep_dropoff_datetime",
		"trip_distance",
		"fare_amount",
		"pickup_zip",
		"dropoff_zip",
	)
	.withColumn("pickup_ts", F.to_timestamp("tpep_pickup_datetime"))
	.withColumn("dropoff_ts", F.to_timestamp("tpep_dropoff_datetime"))
)

show_df(trips, n=20, title="Selected + parsed columns")


# COMMAND ----------
# CELL 5 - Data cleaning + feature engineering
# Adds metrics: duration, fare/mile, speed, and calendar dimensions.
# Filters impossible trips and low-quality records.
trips_clean = (
	trips.withColumn(
		"trip_duration_min",
		(F.col("dropoff_ts").cast("long") - F.col("pickup_ts").cast("long")) / 60.0,
	)
	.withColumn("fare_per_mile", F.col("fare_amount") / F.col("trip_distance"))
	.withColumn("avg_speed_mph", (F.col("trip_distance") / F.col("trip_duration_min")) * 60.0)
	.withColumn("pickup_date", F.to_date("pickup_ts"))
	.withColumn("pickup_hour", F.hour("pickup_ts"))
	.withColumn("pickup_weekday", F.date_format("pickup_ts", "E"))
	.filter(F.col("pickup_ts").isNotNull() & F.col("dropoff_ts").isNotNull())
	.filter(F.col("trip_distance") > 0)
	.filter(F.col("fare_amount") > 0)
	.filter(F.col("trip_duration_min").between(1, 180))
	.filter(F.col("avg_speed_mph").between(1, 80))
)

print(f"Rows after quality filters: {trips_clean.count():,}")
show_df(trips_clean, n=20, title="Cleaned + engineered dataset")


# COMMAND ----------
# CELL 6 - KPI summary
# Single-row business snapshot for overall performance.
kpis = trips_clean.agg(
	F.count("*").alias("total_trips"),
	F.round(F.avg("trip_distance"), 2).alias("avg_distance_mi"),
	F.round(F.avg("trip_duration_min"), 2).alias("avg_duration_min"),
	F.round(F.avg("fare_amount"), 2).alias("avg_fare_usd"),
	F.round(F.avg("fare_per_mile"), 2).alias("avg_fare_per_mile"),
	F.round(F.avg("avg_speed_mph"), 2).alias("avg_speed_mph"),
)

show_df(kpis, n=1, title="KPI summary")


# COMMAND ----------
# CELL 7 - Hourly demand profile
# Trips and fare behavior per pickup hour.
hourly_demand = (
	trips_clean.groupBy("pickup_hour")
	.agg(
		F.count("*").alias("trips"),
		F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
		F.round(F.avg("trip_distance"), 2).alias("avg_distance"),
	)
	.orderBy("pickup_hour")
)

show_df(hourly_demand, n=24, title="Hourly demand and fare profile")


# COMMAND ----------
# CELL 8 - Weekday behavior
# Compares demand and economics across days of week.
weekday_order = F.when(F.col("pickup_weekday") == "Mon", 1) \
	.when(F.col("pickup_weekday") == "Tue", 2) \
	.when(F.col("pickup_weekday") == "Wed", 3) \
	.when(F.col("pickup_weekday") == "Thu", 4) \
	.when(F.col("pickup_weekday") == "Fri", 5) \
	.when(F.col("pickup_weekday") == "Sat", 6) \
	.when(F.col("pickup_weekday") == "Sun", 7)

weekday_stats = (
	trips_clean.groupBy("pickup_weekday")
	.agg(
		F.count("*").alias("trips"),
		F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
		F.round(F.avg("trip_duration_min"), 2).alias("avg_duration_min"),
	)
	.withColumn("weekday_num", weekday_order)
	.orderBy("weekday_num")
	.drop("weekday_num")
)

show_df(weekday_stats, n=7, title="Weekday trip behavior")


# COMMAND ----------
# CELL 9 - Top ZIP areas
# Ranks pickup and dropoff ZIP codes by trips and revenue.
top_pickup_zips = (
	trips_clean.groupBy("pickup_zip")
	.agg(
		F.count("*").alias("trips"),
		F.round(F.sum("fare_amount"), 2).alias("total_fare_usd"),
	)
	.orderBy(F.desc("trips"))
)

top_dropoff_zips = (
	trips_clean.groupBy("dropoff_zip")
	.agg(
		F.count("*").alias("trips"),
		F.round(F.sum("fare_amount"), 2).alias("total_fare_usd"),
	)
	.orderBy(F.desc("trips"))
)

show_df(top_pickup_zips, n=20, title="Top pickup ZIPs")
show_df(top_dropoff_zips, n=20, title="Top dropoff ZIPs")


# COMMAND ----------
# CELL 10 - Most common routes
# Finds high-frequency pickup->dropoff pairs and their avg economics.
route_stats = (
	trips_clean.groupBy("pickup_zip", "dropoff_zip")
	.agg(
		F.count("*").alias("trips"),
		F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
		F.round(F.avg("trip_distance"), 2).alias("avg_distance"),
	)
	.filter(F.col("trips") >= 50)
	.orderBy(F.desc("trips"))
)

show_df(route_stats, n=30, title="Top repeated routes (min 50 trips)")


# COMMAND ----------
# CELL 11 - Distance-band economics
# Buckets trips by distance and compares fare behavior by band.
trips_banded = (
	trips_clean.withColumn(
		"distance_band",
		F.when(F.col("trip_distance") < 1, "<1 mi")
		.when(F.col("trip_distance") < 2, "1-2 mi")
		.when(F.col("trip_distance") < 5, "2-5 mi")
		.when(F.col("trip_distance") < 10, "5-10 mi")
		.otherwise("10+ mi"),
	)
)

distance_band_stats = (
	trips_banded.groupBy("distance_band")
	.agg(
		F.count("*").alias("trips"),
		F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
		F.round(F.avg("fare_per_mile"), 2).alias("avg_fare_per_mile"),
		F.round(F.avg("trip_duration_min"), 2).alias("avg_duration_min"),
	)
	.orderBy(
		F.when(F.col("distance_band") == "<1 mi", 1)
		.when(F.col("distance_band") == "1-2 mi", 2)
		.when(F.col("distance_band") == "2-5 mi", 3)
		.when(F.col("distance_band") == "5-10 mi", 4)
		.otherwise(5)
	)
)

show_df(distance_band_stats, n=10, title="Distance band economics")


# COMMAND ----------
# CELL 12 - High-value trip detection
# Uses p95 fare threshold to isolate premium/outlier rides.
fare_quantiles = trips_clean.approxQuantile("fare_amount", [0.95, 0.99], 0.01)
fare_p95, fare_p99 = fare_quantiles[0], fare_quantiles[1]

print(f"Fare p95: ${fare_p95:.2f} | Fare p99: ${fare_p99:.2f}")

high_value_trips = (
	trips_clean.filter(F.col("fare_amount") >= fare_p95)
	.select(
		"pickup_ts",
		"dropoff_ts",
		"pickup_zip",
		"dropoff_zip",
		"trip_distance",
		"trip_duration_min",
		"fare_amount",
		"fare_per_mile",
	)
	.orderBy(F.desc("fare_amount"))
)

show_df(high_value_trips, n=30, title="High-value trips (>= p95 fare)")


# COMMAND ----------
# CELL 13 - Daily demand trend + moving average
# Creates a smoothed trend signal for demand planning.
daily_trips = (
	trips_clean.groupBy("pickup_date")
	.agg(F.count("*").alias("trips"))
	.orderBy("pickup_date")
)

moving_window = Window.orderBy("pickup_date").rowsBetween(-6, 0)

daily_trips_ma = daily_trips.withColumn(
	"trips_7d_ma",
	F.round(F.avg("trips").over(moving_window), 2),
)

show_df(daily_trips_ma, n=60, title="Daily demand with 7-day moving average")


# COMMAND ----------
# CELL 14 - Auto-generated text insights
# Prints a concise executive summary based on computed tables.
top_hour_row = hourly_demand.orderBy(F.desc("trips")).first()
top_pickup_row = top_pickup_zips.first()
top_route_row = route_stats.first()

print("\n===== Key Insights =====")
if top_hour_row:
	print(
		f"Peak pickup hour: {top_hour_row['pickup_hour']}:00 "
		f"with {top_hour_row['trips']:,} trips and average fare ${top_hour_row['avg_fare']}."
	)

if top_pickup_row:
	print(
		f"Top pickup ZIP: {top_pickup_row['pickup_zip']} "
		f"with {top_pickup_row['trips']:,} trips and ${top_pickup_row['total_fare_usd']:,} total fare."
	)

if top_route_row:
	print(
		f"Most frequent route: {top_route_row['pickup_zip']} -> {top_route_row['dropoff_zip']} "
		f"({top_route_row['trips']:,} trips, avg fare ${top_route_row['avg_fare']}, "
		f"avg distance {top_route_row['avg_distance']} mi)."
	)

print("Use Databricks chart mode on the displayed tables for visual dashboards.")


# COMMAND ----------
# CELL 15 - Visualization cell (Databricks UI)
# Run this cell, then switch each output to Chart in Databricks (bar/line).
# Suggested charts:
# - hourly_demand: Bar chart (x=pickup_hour, y=trips)
# - daily_trips_ma: Line chart (x=pickup_date, y=trips and trips_7d_ma)
# - distance_band_stats: Bar chart (x=distance_band, y=avg_fare_per_mile)
# - top_pickup_zips.limit(10): Bar chart (x=pickup_zip, y=trips)
show_df(hourly_demand, n=24, title="VIS - Hourly trips")
show_df(daily_trips_ma, n=200, title="VIS - Daily demand and 7-day MA")
show_df(distance_band_stats, n=10, title="VIS - Fare per mile by distance band")
show_df(top_pickup_zips.limit(10), n=10, title="VIS - Top 10 pickup ZIPs")


# COMMAND ----------
# CELL 16 - Dynamic controls (Databricks widgets)
# These controls let you interactively filter what is visualized in CELL 17.
# Re-run this cell only if you want to reset widget defaults.
dbutils_available = dbutils is not None

if dbutils_available:
	dbutils.widgets.removeAll()
	dbutils.widgets.dropdown("metric", "trips", ["trips", "avg_fare", "avg_distance"], "Metric")
	dbutils.widgets.text("start_hour", "0", "Start Hour (0-23)")
	dbutils.widgets.text("end_hour", "23", "End Hour (0-23)")
	dbutils.widgets.text("pickup_zip_filter", "ALL", "Pickup ZIP (or ALL)")
	dbutils.widgets.text("top_n", "15", "Top N rows")
	print("Widgets created. Change values in the top widget bar, then run CELL 17.")
else:
	print("dbutils is not available in this environment. Dynamic widgets require Databricks.")



# COMMAND ----------
# CELL 17 - Dynamic visualization output
# Reads widget values, applies filters, and produces chart-ready DataFrames.
# Self-healing: if upstream cells were not run, rebuild required objects.
if "trips_clean" not in globals():
	print("'trips_clean' not found. Rebuilding from source table for this cell...")
	rebuild_raw = spark.table("samples.nyctaxi.trips")
	rebuild_base = (
		rebuild_raw.select(
			"tpep_pickup_datetime",
			"tpep_dropoff_datetime",
			"trip_distance",
			"fare_amount",
			"pickup_zip",
			"dropoff_zip",
		)
		.withColumn("pickup_ts", F.to_timestamp("tpep_pickup_datetime"))
		.withColumn("dropoff_ts", F.to_timestamp("tpep_dropoff_datetime"))
	)

	trips_clean = (
		rebuild_base.withColumn(
			"trip_duration_min",
			(F.col("dropoff_ts").cast("long") - F.col("pickup_ts").cast("long")) / 60.0,
		)
		.withColumn("fare_per_mile", F.col("fare_amount") / F.col("trip_distance"))
		.withColumn("avg_speed_mph", (F.col("trip_distance") / F.col("trip_duration_min")) * 60.0)
		.withColumn("pickup_date", F.to_date("pickup_ts"))
		.withColumn("pickup_hour", F.hour("pickup_ts"))
		.withColumn("pickup_weekday", F.date_format("pickup_ts", "E"))
		.filter(F.col("pickup_ts").isNotNull() & F.col("dropoff_ts").isNotNull())
		.filter(F.col("trip_distance") > 0)
		.filter(F.col("fare_amount") > 0)
		.filter(F.col("trip_duration_min").between(1, 180))
		.filter(F.col("avg_speed_mph").between(1, 80))
	)

if "moving_window" not in globals():
	moving_window = Window.orderBy("pickup_date").rowsBetween(-6, 0)

if dbutils_available:
	metric = dbutils.widgets.get("metric")
	start_hour = int(dbutils.widgets.get("start_hour"))
	end_hour = int(dbutils.widgets.get("end_hour"))
	pickup_zip_filter = dbutils.widgets.get("pickup_zip_filter")
	top_n = int(dbutils.widgets.get("top_n"))
else:
	metric = "trips"
	start_hour = 0
	end_hour = 23
	pickup_zip_filter = "ALL"
	top_n = 15

start_hour = max(0, min(23, start_hour))
end_hour = max(0, min(23, end_hour))
if start_hour > end_hour:
	start_hour, end_hour = end_hour, start_hour

zip_filtered = trips_clean
if pickup_zip_filter.upper() != "ALL":
	zip_filtered = zip_filtered.filter(F.col("pickup_zip").cast("string") == pickup_zip_filter)

dynamic_hourly = (
	zip_filtered.filter(F.col("pickup_hour").between(start_hour, end_hour))
	.groupBy("pickup_hour")
	.agg(
		F.count("*").alias("trips"),
		F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
		F.round(F.avg("trip_distance"), 2).alias("avg_distance"),
	)
	.orderBy("pickup_hour")
)

dynamic_top_zips = (
	zip_filtered.groupBy("pickup_zip")
	.agg(
		F.count("*").alias("trips"),
		F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
		F.round(F.avg("trip_distance"), 2).alias("avg_distance"),
	)
	.orderBy(F.desc(metric))
	.limit(top_n)
)

dynamic_daily = (
	zip_filtered.groupBy("pickup_date")
	.agg(F.count("*").alias("trips"))
	.orderBy("pickup_date")
	.withColumn("trips_7d_ma", F.round(F.avg("trips").over(moving_window), 2))
)

print(
	f"Dynamic view -> metric={metric}, hour_range={start_hour}-{end_hour}, "
	f"pickup_zip={pickup_zip_filter}, top_n={top_n}"
)

show_df(dynamic_hourly, n=24, title="DYNAMIC VIS - Hourly profile")
show_df(dynamic_top_zips, n=top_n, title=f"DYNAMIC VIS - Top ZIPs by {metric}")
show_df(dynamic_daily, n=200, title="DYNAMIC VIS - Daily trend + 7d MA")

# Tip in Databricks: set chart type once for each output, then just re-run CELL 17 after changing widgets.


# COMMAND ----------
# CELL 18 - Dynamic graphical visualization (interactive)
# This cell renders interactive charts (zoom, pan, hover tooltips, legend toggles).
# Re-run CELL 17 first whenever widgets change, then run this cell.
try:
	import plotly.express as px
	plotly_available = True
except Exception:
	plotly_available = False

if not plotly_available:
	print("Plotly is not available in this cluster. Install it with: %pip install plotly")
elif "dynamic_hourly" not in globals() or "dynamic_top_zips" not in globals() or "dynamic_daily" not in globals():
	print("Run CELL 17 first so dynamic DataFrames are created.")
else:
	# Convert to Pandas for Plotly rendering (small, chart-friendly slices)
	hourly_pd = dynamic_hourly.toPandas()
	top_zips_pd = dynamic_top_zips.toPandas()
	daily_pd = dynamic_daily.limit(500).toPandas()

	fig_hourly = px.bar(
		hourly_pd,
		x="pickup_hour",
		y=metric,
		title=f"Hourly profile ({metric}) - filtered",
		labels={"pickup_hour": "Pickup hour", metric: metric.replace("_", " ").title()},
	)

	fig_daily = px.line(
		daily_pd,
		x="pickup_date",
		y=["trips", "trips_7d_ma"],
		title="Daily trips vs 7-day moving average",
		labels={"value": "Trips", "pickup_date": "Date", "variable": "Series"},
	)

	fig_top_zips = px.bar(
		top_zips_pd,
		x="pickup_zip",
		y=metric,
		title=f"Top pickup ZIPs by {metric}",
		labels={"pickup_zip": "Pickup ZIP", metric: metric.replace("_", " ").title()},
	)

	for fig in [fig_hourly, fig_daily, fig_top_zips]:
		fig.update_layout(template="plotly_white", hovermode="x unified")

	# Databricks can render plotly figures with display(); local fallback uses fig.show().
	display_fn = globals().get("display")
	if callable(display_fn):
		display_fn(fig_hourly)
		display_fn(fig_daily)
		display_fn(fig_top_zips)
	else:
		fig_hourly.show()
		fig_daily.show()
		fig_top_zips.show()


# COMMAND ----------
# CELL 19 - Animated graph (moving visualization + hover info)
# This chart animates by pickup hour and shows trip volume + fare details by weekday.
# Run CELL 17 first (so filters/widgets are applied), then run this cell.
try:
	import plotly.express as px
	plotly_available = True
except Exception:
	plotly_available = False

if not plotly_available:
	print("Plotly is not available in this cluster. Install it with: %pip install plotly")
elif "zip_filtered" not in globals():
	print("Run CELL 17 first so filtered data is ready for animation.")
else:
	animated_base = (
		zip_filtered.groupBy("pickup_hour", "pickup_weekday")
		.agg(
			F.count("*").alias("trips"),
			F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
			F.round(F.avg("trip_distance"), 2).alias("avg_distance"),
		)
	)

	weekday_sort = F.when(F.col("pickup_weekday") == "Mon", 1) \
		.when(F.col("pickup_weekday") == "Tue", 2) \
		.when(F.col("pickup_weekday") == "Wed", 3) \
		.when(F.col("pickup_weekday") == "Thu", 4) \
		.when(F.col("pickup_weekday") == "Fri", 5) \
		.when(F.col("pickup_weekday") == "Sat", 6) \
		.when(F.col("pickup_weekday") == "Sun", 7)

	animated_pd = (
		animated_base.withColumn("weekday_num", weekday_sort)
		.orderBy("pickup_hour", "weekday_num")
		.toPandas()
	)

	fig_animated = px.scatter(
		animated_pd,
		x="pickup_weekday",
		y="trips",
		size="avg_fare",
		color="avg_distance",
		animation_frame="pickup_hour",
		animation_group="pickup_weekday",
		hover_data={
			"pickup_weekday": True,
			"trips": ":,",
			"avg_fare": ":.2f",
			"avg_distance": ":.2f",
			"pickup_hour": True,
		},
		title="Animated demand by weekday (hour-by-hour)",
		labels={
			"pickup_weekday": "Weekday",
			"trips": "Trips",
			"avg_fare": "Avg fare ($)",
			"avg_distance": "Avg distance (mi)",
			"pickup_hour": "Pickup hour",
		},
		range_y=[0, max(1, animated_pd["trips"].max() * 1.1)],
	)

	fig_animated.update_layout(template="plotly_white")
	fig_animated.update_xaxes(categoryorder="array", categoryarray=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

	# Set smoother playback speed for the moving animation.
	fig_animated.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 550
	fig_animated.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 300

	# Force autoplay in Databricks using HTML rendering.
	display_html_fn = globals().get("displayHTML")
	html = fig_animated.to_html(full_html=False, include_plotlyjs="cdn", auto_play=True)
	if callable(display_html_fn):
		display_html_fn(html)
	else:
		display_fn = globals().get("display")
		if callable(display_fn):
			display_fn(fig_animated)
		else:
			fig_animated.show()


# COMMAND ----------
# CELL 20 - Autoplay animated graph + insight highlights
# This animation auto-plays in Databricks and shows how hourly demand changes by day.
# Run CELL 17 first (for filters), then run this cell.
try:
	import plotly.express as px
	plotly_available = True
except Exception:
	plotly_available = False

if not plotly_available:
	print("Plotly is not available in this cluster. Install it with: %pip install plotly")
elif "zip_filtered" not in globals():
	print("Run CELL 17 first so filtered data is ready.")
else:
	animated_day_hour = (
		zip_filtered.groupBy("pickup_date", "pickup_hour")
		.agg(
			F.count("*").alias("trips"),
			F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
			F.round(F.avg("avg_speed_mph"), 2).alias("avg_speed_mph"),
		)
		.orderBy("pickup_date", "pickup_hour")
	)

	anim_pd = animated_day_hour.toPandas()
	if anim_pd.empty:
		print("No rows available for the selected filters.")
	else:
		anim_pd["pickup_date"] = anim_pd["pickup_date"].astype(str)

		# Insight 1: date with maximum total trips in the filtered slice
		peak_day = (
			anim_pd.groupby("pickup_date", as_index=False)["trips"]
			.sum()
			.sort_values("trips", ascending=False)
			.iloc[0]
		)

		# Insight 2: most frequent peak hour across days
		peak_hour_by_day = (
			anim_pd.sort_values(["pickup_date", "trips"], ascending=[True, False])
			.groupby("pickup_date", as_index=False)
			.first()[["pickup_date", "pickup_hour"]]
		)
		most_common_peak_hour = int(peak_hour_by_day["pickup_hour"].mode().iloc[0])

		print("\n=== Animated Insights ===")
		print(f"Highest-demand day: {peak_day['pickup_date']} ({int(peak_day['trips']):,} trips)")
		print(f"Most common peak hour across days: {most_common_peak_hour}:00")

		fig_day_hour = px.bar(
			anim_pd,
			x="pickup_hour",
			y="trips",
			animation_frame="pickup_date",
			animation_group="pickup_hour",
			color="avg_fare",
			hover_data={
				"pickup_hour": True,
				"trips": ":,",
				"avg_fare": ":.2f",
				"avg_speed_mph": ":.2f",
				"pickup_date": True,
			},
			title="Autoplay animation: hourly demand by day (color = avg fare)",
			labels={
				"pickup_hour": "Pickup hour",
				"trips": "Trips",
				"avg_fare": "Avg fare ($)",
				"avg_speed_mph": "Avg speed (mph)",
				"pickup_date": "Date",
			},
			range_y=[0, max(1, anim_pd["trips"].max() * 1.15)],
		)

		fig_day_hour.update_layout(template="plotly_white", bargap=0.15)
		if fig_day_hour.layout.updatemenus and fig_day_hour.layout.updatemenus[0].buttons:
			fig_day_hour.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 450
			fig_day_hour.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 250

		# Force true animation rendering in Databricks via HTML autoplay.
		display_html_fn = globals().get("displayHTML")
		html = fig_day_hour.to_html(full_html=False, include_plotlyjs="cdn", auto_play=True)
		if callable(display_html_fn):
			display_html_fn(html)
		else:
			display_fn = globals().get("display")
			if callable(display_fn):
				display_fn(fig_day_hour)
			else:
				fig_day_hour.show()
