import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange

pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 500)
sns.set_style("darkgrid")
plt.isinteractive()

##################### SET EXPERIMENT DATES HERE #######################################

# Is surplus utilization active? Then set this to True.
surplus_utilization = True

# Set the start and end time and date of the experiment to select data from the csv log
# single day
start_date_1 = '2021-06-21 03:00:00'
end_date_1 = '2021-06-22 03:00:00'

# 7-day interval
start_date_7 = '2021-06-20 20:00:00'
end_date_7 = '2021-06-27 21:00:00'

#######################################################################################


df = pd.read_csv("grid.csv")
df['timestamp'] = pd.to_datetime((df['timestamp']))


def calculate_computation_base_values(df):
    # Cumulated computations
    df['computations_cumulated'] = 0
    for i in range(1, len(df)):
        if df.at[i, "event"] in ["wakeup", "start_compute", "shutdown"]:
            pass
        if df.at[i, "event"] == "unit_computed":
            df.at[i, 'computations_cumulated'] = df.at[i - 1, 'computations_cumulated'] + 1
        if df.at[i, "event"] == "shutdown":
            df.at[i, "computations_cumulated"] = df.at[i - 1, 'computations_cumulated']

    # Add time used for computations
    df['computation_time'] = pd.Timedelta("0 days")
    for i in range(1, len(df)):
        # look for start_compute time
        if df.at[i, "event"] == "start_compute":
            start_compute_time = df.loc[i].timestamp
        # look for stop_compute time
        if df.at[i, "event"] == "stop_compute":
            stop_compute_time = df.loc[i].timestamp
            df.at[i, 'computation_time'] = stop_compute_time - start_compute_time


def calculate_time_above_battery_level_x(df, x):
    varname = "surplus_time_" + str(x)
    df[varname] = pd.Timedelta("0 days")
    for i in range(1, len(df)):
        # values for interpolation
        value_1 = df.at[i, "battery_level"]
        value_0 = df.at[i - 1, "battery_level"]
        delta = value_1 - value_0
        diff_1 = value_1 - x
        diff_0 = x - value_0
        t_1 = df.loc[i].timestamp
        t_0 = df.loc[i - 1].timestamp
        time_delta = t_1 - t_0
        interpolation_factor = 1 / (delta / (diff_1 / (diff_1 + diff_0)))

        if value_1 < x:
            df.at[i, varname] = pd.Timedelta("0 days")
        elif (value_0 >= x) & (value_1 >= x):
            df.at[i, varname] = time_delta
        # interpolate time to account for large jumps from below x to above x
        elif (value_0 < x) & (value_1 >= x):
            df.at[i, varname] = interpolation_factor * time_delta


# # Calculate time above 98% battery level
# df['surplus_time_98'] = pd.Timedelta("0 days")
# for i in range(1, len(df)):
#     if df.at[i, "battery_level"] < 98:
#         df.at[i, 'surplus_time_98'] = pd.Timedelta("0 days")
#     # add another interpolation for cases where <98 but before was >= 98
#     elif (df.at[i, "battery_level"] >= 98) & (df.at[i - 1, "battery_level"] < 98):
#         df.at[i, 'surplus_time_98'] = (df.loc[i].timestamp - df.loc[i - 1].timestamp) / 2  # interpolate
#     elif (df.at[i, "battery_level"] >= 98) & (df.at[i - 1, "battery_level"] >= 98):
#         df.at[i, 'surplus_time_98'] = df.loc[i].timestamp - df.loc[i - 1].timestamp
#
# # Calculate time above 95% battery level
# df['surplus_time_95'] = pd.Timedelta("0 days")
# for i in range(1, len(df)):
#     if df.at[i, "battery_level"] < 95:
#         df.at[i, 'surplus_time_95'] = pd.Timedelta("0 days")
#     # add another interpolation for cases where <95 but before was >= 95
#     elif (df.at[i, "battery_level"] >= 95) & (df.at[i - 1, "battery_level"] < 95):
#         df.at[i, 'surplus_time_95'] = (df.loc[i].timestamp - df.loc[i - 1].timestamp) / 2  # interpolate
#     elif (df.at[i, "battery_level"] >= 95) & (df.at[i - 1, "battery_level"] >= 95):
#         df.at[i, 'surplus_time_95'] = df.loc[i].timestamp - df.loc[i - 1].timestamp
#
# # Calculate time above 85% battery level
# df['surplus_time_85'] = pd.Timedelta("0 days")
# for i in range(1, len(df)):
#     if df.at[i, "battery_level"] < 85:
#         df.at[i, 'surplus_time_85'] = pd.Timedelta("0 days")
#     # add another interpolation for cases where <95 but before was >= 95
#     elif (df.at[i, "battery_level"] >= 85) & (df.at[i - 1, "battery_level"] < 85):
#         df.at[i, 'surplus_time_85'] = (df.loc[i].timestamp - df.loc[i - 1].timestamp) / 2  # interpolate
#     elif (df.at[i, "battery_level"] >= 85) & (df.at[i - 1, "battery_level"] >= 85):
#         df.at[i, 'surplus_time_85'] = df.loc[i].timestamp - df.loc[i - 1].timestamp

calculate_computation_base_values(df)

calculate_time_above_battery_level_x(df, 85)
calculate_time_above_battery_level_x(df, 95)
calculate_time_above_battery_level_x(df, 98)

df = df.set_index('timestamp')

# Create sub-dataframes for different start and end dates chosen above
df_single_day = df.loc[start_date_1:end_date_1]
df_seven_days = df.loc[start_date_7:end_date_7]


def calculate_stats(data):
    stats = dict()
    stats["experiment_duration"] = data.index[-1] - data.index[0]
    stats["start_date"] = data.index[0]
    stats["end_date"] = data.index[-1]

    # Battery stats
    stats["max_battery_level"] = max(data.battery_level)
    stats["min_battery_level"] = min(data.battery_level)
    # For the mean battery level, resample hourly and calculate the mean of all hourly average temperatures
    stats["mean_battery_level"] = data.battery_level.resample('60min').mean().mean()

    stats["battery_above_98_absolute"] = data.surplus_time_98.sum()
    stats["battery_above_98 relative"] = stats["battery_above_98_absolute"] / stats["experiment_duration"]

    stats["battery_above_95_absolute"] = data.surplus_time_95.sum()
    stats["battery_above_95 relative"] = stats["battery_above_95_absolute"] / stats["experiment_duration"]

    stats["battery_above_85_absolute"] = data.surplus_time_85.sum()
    stats["battery_above_85 relative"] = stats["battery_above_85_absolute"] / stats["experiment_duration"]

    # Computation stats
    stats["computations_absolute"] = data.event.value_counts().unit_computed
    stats["mean_computations_24h"] = stats["computations_absolute"] / (
            stats["experiment_duration"] / pd.Timedelta(days=1))

    stats["computation_time_absolute"] = data.computation_time.sum()
    stats["computation_time_relative"] = stats["computation_time_absolute"] / stats["experiment_duration"]
    stats["computation_rate"] = stats["computations_absolute"] / (
            stats["computation_time_absolute"].total_seconds() / 60)

    # Temperature stats
    stats["max_temperature"] = max(data.battery_temperature)
    stats["min_temperature"] = min(data.battery_temperature)

    # For the mean temperature, resample hourly and then calculate the mean of the hourly average temperature
    stats["mean_temperature"] = data.battery_temperature.resample('60min').mean().mean()
    return stats


print("----------- 1 day -----------")

for item in calculate_stats(df_single_day).items():
    print(item)

print("----------- 7 days -----------")

for item in calculate_stats(df_seven_days).items():
    print(item)

#####################

# set font sizes
plt.rc('axes', labelsize=15)
plt.rc('xtick', labelsize=15)
plt.rc('ytick', labelsize=15)
plt.rc('legend', fontsize=15)


def create_plots(data, filename, surplus_utilization, duration):
    fig, ax1 = plt.subplots(figsize=(16, 4), dpi=200)
    lns1 = ax1.plot_date(data.index, data.battery_level, color='blue', marker='.', alpha=0.5, linestyle=':',
                         markersize=2, label='battery_level', dash_capstyle='round', linewidth=1)
    lns2 = ax1.plot_date(data.index, data.battery_temperature, color='orange', marker='.', alpha=0.5, linestyle=':',
                         markersize=2, label='battery_temperature', dash_capstyle='round', linewidth=1)

    ax1.set_xlim([min(data.index), max(data.index)])

    ax1.set_ylabel('Battery Level (%), Temperature (°C)')
    ax1.set_ylim(0, 105)
    ax1.set_yticks([0, 25, 50, 65, 85, 98])

    ax1.axhline(y=85, color="black", linestyle='--', alpha=0.5, label='85%')
    ax1.axhline(y=98, color="red", linestyle='--', alpha=0.5, label='98%')

    if duration == "long":
        ax1.xaxis.set_major_locator(DayLocator())
    else:
        ax1.xaxis.set_major_locator(HourLocator(interval=2))
    # ax1.fmt_xdata = DateFormatter('% Y-% m-% d % H:% M:% S')

    if surplus_utilization:
        ax2 = ax1.twinx()

        lns3 = ax2.plot(data.computations_cumulated, color='green', marker='.', alpha=0.5, linestyle=':', markersize=2,
                        label='units_computed', dash_capstyle='round', linewidth=1)

        ax2.set_ylabel('Units')
        ax2.set_ylim(0, max(data['computations_cumulated']) * 1.10)

    # Create a single legend
    lns = lns1 + lns2
    if surplus_utilization:
        lns += lns3

    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, markerscale=8, bbox_to_anchor=(0, 1, 1, 0), loc="lower center", ncol=3)

    # Rotate and autoalign the labels
    fig.autofmt_xdate()

    plt.rcParams['axes.axisbelow'] = True
    plt.savefig(filename, bbox_inches="tight")
    # plt.show()


create_plots(df_single_day, "plot1_single_day", surplus_utilization, duration="short")
create_plots(df_seven_days, "plot2_seven_days", surplus_utilization, duration="long")
