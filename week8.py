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
    # Drop duplicates
    df = df.drop_duplicates()

    # Handle missing values
    if 'title' in df.columns:
        df = df.dropna(subset=['title'])  # Drop rows where title is missing

    if 'publish_time' in df.columns and pd.api.types.is_numeric_dtype(df['publish_time']):
        df['publish_time'] = df['publish_time'].fillna(df['publish_time'].median())  # Fill missing years with median year

    # Standardize text data
    if 'title' in df.columns and df['title'].dtype == object:
        df['title'] = df['title'].str.title()
    if 'authors' in df.columns and df['authors'].dtype == object:
        df['authors'] = df['authors'].str.title()

    return df



# ---------------- VISUALIZATIONS ---------------- #
def papers_per_year(df):
    df['year'] = pd.to_datetime(df['publish_time'], errors='coerce').dt.year
    papers_per_year = df['publish_time'].value_counts().sort_index()

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
    df['year'] = pd.to_datetime(df['publish_time'], errors='coerce').dt.year
    year_counts = df['publish_time'].value_counts().sort_index()

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

    # --- Visualizations ---
    st.header("Papers Published Per Year")
    papers_per_year(cleaned_df)

    st.header("Top Journals by Number of Publications")
    plot_top_journals(cleaned_df, top_n=10)

    st.header("Publications by Country")
    plot_publications_by_country(cleaned_df)

    st.header("Publications by Year")
    plot_publications_by_year(cleaned_df)


    
if __name__ == "__main__":
    main()
