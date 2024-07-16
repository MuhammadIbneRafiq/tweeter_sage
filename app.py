import streamlit as st
import pandas as pd
import asyncio
import concurrent.futures
from ntscraper import Nitter
from streamlit_chat import message

# Function to initialize Nitter scraper asynchronously
def init_nitter():
    return Nitter(0)

async def async_init_nitter():
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, init_nitter)
    return result

async def fetch_tweets(scraper, name, mode, number):
    loop = asyncio.get_event_loop()
    tweets = await loop.run_in_executor(None, scraper.get_tweets, name, mode, number)
    return tweets

def get_tweet_data(tweets):
    final_tweets = []
    for x in tweets['tweets']:
        data = [x['link'], x['text'], x['date'], x['stats']['likes'], x['stats']['comments']]
        final_tweets.append(data)
    return pd.DataFrame(final_tweets, columns=['twitter_link', 'text', 'date', 'likes', 'comments'])

async def main():
    st.set_page_config(page_title="Freelancer Finder", layout="wide")

    # Title and Sidebar
    st.title("Meet AutoLanding AI, Your Personal Agent to Find Affordable and Talented Freelancers")

    st.sidebar.image("./twitter_scraped_client.png", use_column_width=True)

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    with st.spinner("Initializing scraper..."):
        scraper = await async_init_nitter()

    # Main chat interface
    st.subheader("Chats")

    chat_input = st.text_input("Type a keyword and press Enter", "")
    if chat_input:
        st.session_state.messages.append(chat_input)
        chat_input = ""

    if st.session_state.messages:
        for msg in st.session_state.messages:
            message(msg, is_user=True)

            with st.spinner("Fetching data..."):
                tweets = await fetch_tweets(scraper, msg, 'hashtag', 5)
                data = get_tweet_data(tweets)

            if not data.empty:
                for i, row in data.iterrows():
                    st.write(f"**{row['date']}**")
                    st.write(row['text'])
                    st.write(f"Likes: {row['likes']} | Comments: {row['comments']}")
                    st.write(f"[Link to Tweet]({row['twitter_link']})")
                    st.write("---")
            else:
                st.warning("No tweets found for the given query.")

if __name__ == "__main__":
    asyncio.run(main())
