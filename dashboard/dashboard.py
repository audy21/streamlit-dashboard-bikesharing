import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the combined dataset
all_df = pd.read_csv('../dashboard/all_data.csv')

# Konversi kolom 'dteday' (asumsi nama kolom yang menyimpan tanggal) menjadi format datetime
all_df['dteday'] = pd.to_datetime(all_df['dteday'], errors='coerce')

# Title
st.title("Bike Sharing Analysis Dashboard")

# Sidebar untuk filter rentang tanggal
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", all_df['dteday'].min())
end_date = st.sidebar.date_input("End Date", all_df['dteday'].max())

# Filter data berdasarkan rentang tanggal
filtered_df = all_df[(all_df['dteday'] >= pd.to_datetime(start_date)) & (all_df['dteday'] <= pd.to_datetime(end_date))]

# Cek apakah ada data setelah difilter
if filtered_df.empty:
    st.warning("No data available for the selected date range.")
else:
    # Trend Chart
    st.subheader("Trend of Bicycle Users Over Time")
    
    # Ubah dteday menjadi format bulanan string
    filtered_df['month_year'] = filtered_df['dteday'].dt.strftime('%Y-%m')
    
    # Kelompokkan berdasarkan bulanan
    monthly_counts = filtered_df.groupby('month_year').agg({"cnt": "sum"}).reset_index()
    
    sns.lineplot(data=monthly_counts, x='month_year', y='cnt', marker="o")
    plt.title("Trend Bicycle Users Over Time")
    plt.xlabel("Month-Year")
    plt.ylabel("Total Users")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    st.pyplot(plt)

    # Season Pattern Chart
    st.subheader("Pattern of Bike Rentals by Season")
    season_pattern = filtered_df.groupby('season')[['registered', 'casual']].sum().reset_index()
    plt.figure(figsize=(10, 6))
    plt.bar(season_pattern['season'], season_pattern['registered'], label='Registered', color='tab:red')
    plt.bar(season_pattern['season'], season_pattern['casual'], label='Casual', color='tab:blue')
    plt.xlabel("Season")
    plt.ylabel("Users")
    plt.title('Number of Bicycle Renters Based on Season')
    plt.legend()
    st.pyplot(plt)

    # Weather Pattern Chart
    st.subheader("Pattern of Bike Rentals by Weather")
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='weathersit', y='cnt', data=filtered_df, hue='weathersit', palette='viridis', dodge=False, width=0.6)

    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 10),
                    textcoords='offset points')

    plt.title('Number of Bicycle Users by Weather Conditions', fontsize=16)
    plt.xlabel('Weather Conditions', fontsize=12)
    plt.ylabel('Bicycle Users', fontsize=12)
    weather_labels = ['Clear', 'Mist + Cloudy', 'Light Snow/Rain', 'Heavy Rain/Snow']
    plt.xticks(range(len(weather_labels)), weather_labels, fontsize=10)
    plt.yticks(fontsize=10)
    sns.despine()
    plt.legend([], [], frameon=False)
    st.pyplot(plt)

    # Holiday vs. Weekday Chart
    st.subheader("Comparison of Bike Rentals Between Holidays and Weekdays")
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='workingday', y='cnt', data=filtered_df, hue='workingday', palette="Set2", legend=False, dodge=False, width=0.5)

    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 10),
                    textcoords='offset points')

    plt.title('Comparing Bicycle Users Between Working Days and Non-Working Days', fontsize=16)
    plt.xlabel(None)
    plt.ylabel('Users', fontsize=12)
    plt.xticks([0, 1], ['Non-Working Day', 'Working Day'], fontsize=12)
    plt.yticks(fontsize=10)
    sns.despine()
    st.pyplot(plt)

    # Daily Rentals Comparison Chart
    st.subheader("Comparison of Daily Bike Rentals")
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='weathersit', y='cnt', data=filtered_df, hue='weathersit', palette="Spectral", legend=False, dodge=False, width=0.6)

    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 10),
                    textcoords='offset points')

    plt.title('Number of Bicycle Users based on Weather Conditions', fontsize=16)
    plt.xlabel('Weather Conditions', fontsize=12)
    plt.ylabel('Number of Bicycle Users', fontsize=12)
    plt.xticks([0, 1, 2], ['Clear', 'Mist + Cloudy', 'Light Snow/Rain'], fontsize=10)
    plt.yticks(fontsize=10)
    sns.despine()
    st.pyplot(plt)
