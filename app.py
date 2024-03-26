import streamlit as st
import urllib.parse
from datetime import datetime, timedelta

def generate_google_calendar_url(event_details):
    try:
        # Attempt to extract datetime and title from the event details
        details_parts = event_details.split(' ', 2)
        if len(details_parts) < 3:
            raise ValueError("Format must include date, time, and title.")
        
        event_date, event_time, event_title = details_parts[0], details_parts[1], details_parts[2]
        event_datetime_str = f"{event_date} {event_time}"
        event_datetime = datetime.strptime(event_datetime_str, '%Y-%m-%d %H:%M')
        start_time = event_datetime.strftime('%Y%m%dT%H%M00')
        end_time = (event_datetime + timedelta(hours=1)).strftime('%Y%m%dT%H%M00')  # Default duration 1 hour
        
        # Create the Google Calendar URL
        base_url = "https://calendar.google.com/calendar/render"
        params = {
            'action': 'TEMPLATE',
            'text': event_title,
            'dates': f'{start_time}/{end_time}',
            'details': 'Added from Streamlit App',
        }
        url_params = urllib.parse.urlencode(params)
        return f"{base_url}?{url_params}"
    except ValueError as e:
        st.error(str(e))
        return None

# Streamlit UI
st.title('Add Event to Google Calendar')

# User input for event details
event_details = st.text_input('Enter event details (Format: "YYYY-MM-DD HH:MM Event Title")', '')

# Add to Google Calendar button
if st.button(f'Add to Google Calendar 📅'):
    calendar_url = generate_google_calendar_url(event_details)
    if calendar_url:
        st.markdown(f'<a target="_blank" href="{calendar_url}">Open Google Calendar</a>', unsafe_allow_html=True)
        st.write('If the link does not open automatically, please click the above link to add the event manually.')
