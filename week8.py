import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load dataset

url = "https://drive.google.com/uc?id=1nism0Up8FAiO8ALBv4t-tPJ6h8yUcoIK"
df = pd.read_csv(url, on_bad_lines='skip')

# Ensure consistent data types
for col in df.columns:
    if df[col].map(type).nunique() > 1:
        try:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        except:
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except:
                df[col] = df[col].astype(str)


# ---------------- DATA CLEANING ---------------- #
def clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna(method='ffill').fillna(method='bfill')

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        mean = df[col].mean()
        std = df[col].std()
        df = df[(df[col] >= mean - 3 * std) & (df[col] <= mean + 3 * std)]

    return df


# ---------------- VISUALIZATIONS ---------------- #
def papers_per_year(df):
    df['year'] = pd.to_datetime(df['year'], errors='coerce').dt.year
    papers_per_year = df['year'].value_counts().sort_index()

    plt.figure(figsize=(10, 5))
    plt.plot(papers_per_year.index, papers_per_year.values, marker='o')
    plt.title('Number of Papers Published Per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Papers')
    plt.grid(True)
    st.pyplot(plt)


def plot_publications_by_country(df):
    country_counts = df['country'].value_counts()

    plt.figure(figsize=(10, 5))
    country_counts.plot(kind='bar')
    plt.title('Number of Publications by Country')
    plt.xlabel('Country')
    plt.ylabel('Number of Publications')
    plt.xticks(rotation=45)
    st.pyplot(plt)


def plot_publications_by_year(df):
    df['year'] = pd.to_datetime(df['year'], errors='coerce').dt.year
    year_counts = df['year'].value_counts().sort_index()

    plt.figure(figsize=(10, 5))
    year_counts.plot(kind='line', marker='o')
    plt.title('Number of Publications by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Publications')
    plt.grid(True)
    st.pyplot(plt)


def plot_top_journals(df, top_n=10):
    top_journals = df['journal'].value_counts().head(top_n)
    plt.figure(figsize=(10, 5))
    top_journals.plot(kind='bar')
    plt.title(f'Top {top_n} Journals by Number of Publications')
    plt.xlabel('Journal')
    plt.ylabel('Number of Publications')
    plt.xticks(rotation=45)
    st.pyplot(plt)


# ---------------- MAIN APP ---------------- #
def main():
    st.title("📊 Research Publications Analysis")

    # Clean dataset
    cleaned_df = clean_data(df)

    # --- Sidebar Filters ---
    st.sidebar.header("🔎 Filters")

    # Filter by Year
    cleaned_df['year'] = pd.to_datetime(cleaned_df['year'], errors='coerce').dt.year
    available_years = sorted(cleaned_df['year'].dropna().unique())
    selected_years = st.sidebar.multiselect("Select Year(s)", available_years, default=available_years)

    # Filter by Country
    available_countries = sorted(cleaned_df['country'].dropna().unique())
    selected_countries = st.sidebar.multiselect("Select Country/Countries", available_countries, default=available_countries)

    # Apply Filters
    filtered_df = cleaned_df[
        (cleaned_df['year'].isin(selected_years)) &
        (cleaned_df['country'].isin(selected_countries))
    ]

    # --- Show Data Preview ---
    st.subheader("Preview of Filtered Data")
    st.dataframe(filtered_df.head())

    # --- Visualizations ---
    if not filtered_df.empty:
        st.header("Papers Published Per Year")
        papers_per_year(filtered_df)

        st.header("Top Journals by Number of Publications")
        plot_top_journals(filtered_df, top_n=10)

        st.header("Publications by Country")
        plot_publications_by_country(filtered_df)

        st.header("Publications by Year")
        plot_publications_by_year(filtered_df)
    else:
        st.warning("⚠️ No data available for the selected filters.")


if __name__ == "__main__":
    main()
