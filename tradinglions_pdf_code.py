#Final script adjusted :Daily outlook including 4 parts to analyse financialy the markets

from fpdf import FPDF
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import feedparser

# Custom PDF class to include logo, headers, footers, and borders
class PDF(FPDF):
    def __init__(self, logo_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logo_path = logo_path

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Weekly Forex Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Date: {datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'C')
        self.ln(10)
        self.image(self.logo_path, 10, 8, 33)  # Add logo

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_page_with_borders(self):
        self.add_page()
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.5)
        self.rect(5, 5, self.w - 10, self.h - 10, 'D')

    def add_event_table(self, events):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Event Details', 0, 1)
        self.set_font('Arial', 'B', 10)
        self.cell(80, 10, 'Title', 1)
        self.cell(30, 10, 'Previous', 1)
        self.cell(30, 10, 'Consensus', 1)
        self.cell(30, 10, 'Actual', 1)
        self.ln()
        self.set_font('Arial', '', 10)
        for event in events:
            self.cell(80, 10, event['title'], 1)
            self.cell(30, 10, event['previous'], 1)
            self.cell(30, 10, event['consensus'], 1)
            self.cell(30, 10, event['actual'], 1)
            self.ln()


# Function to download an image from a URL
def download_image(url, image_path):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(image_path)


def table_of_contents(pdf):
    # Add a placeholder TOC at the beginning
    pdf.add_page_with_borders()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Table of Contents', 0, 1, 'C')
    pdf.ln(10)

    # Placeholder for the TOC entries with short descriptions
    contents = [
        ('1. Economic Calendar', 'Upcoming Events'),
        ('2. Personal Analysis', 'Dollar Index (DXY)'),
        ('3. Personal Analysis2', 'Trade Ideas'),
        ('4. Headlines', 'Market News'),
        ('5. Macroeconomic Graphs', 'Key Indicators')
    ]

    # Setting up the table
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(140, 10, 'Section', 1)
    pdf.cell(50, 10, 'Description', 1)
    pdf.ln()

    pdf.set_font('Arial', '', 12)
    for entry, description in contents:
        pdf.cell(140, 10, entry, 1)
        pdf.cell(50, 10, description, 1)
        pdf.ln()


def economic_calendar(pdf):
    url = "https://www.myfxbook.com/rss/forex-economic-calendar-events"
    response = requests.get(url)
    rss_content = response.content
    soup = BeautifulSoup(rss_content, 'xml')
    economic_calendar_items = soup.find_all('item')

    keywords = ['US', 'USA', 'America', 'American', 'United States', 
                'UK', 'United Kingdom', 'Britain', 'British',
                'Eurozone', 'Europe', 'European', 
                'Japan', 'JPY', 'Yen',
                'CPI', 'NFP', 'Non Farm Payrolls', 
                'Inflation Rate YoY', 'Inflation Rate MoM', 
                'Core Inflation Rate MoM', 'Core Inflation Rate YoY']

    # Specific countries of interest
    countries_of_interest = ['United States', 'Eurozone', 'United Kingdom', 'Japan']

    filtered_entries = []

    for item in economic_calendar_items:
        title = item.find('title')
        description = item.find('description')
        if title and description:
            title_text = title.text

            # Check if the event matches the keywords and is from the specified countries
            if any(keyword in title_text for keyword in keywords):
                if any(country in title_text for country in countries_of_interest):
                    desc_soup = BeautifulSoup(description.text, 'html.parser')
                    table_row = desc_soup.find_all('tr')[1]
                    values = [td.text.strip() for td in table_row.find_all('td')]
                    previous = values[2]
                    consensus = values[3]
                    actual = values[4]
                    filtered_entries.append({
                        'title': title_text,
                        'previous': previous,
                        'consensus': consensus,
                        'actual': actual
                    })

    pdf.add_page_with_borders()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Economic Calendar', 0, 1, 'C')
    pdf.ln(10)
    pdf.add_event_table(filtered_entries)

def trade_ideas(pdf):
    # Add a page with borders
    pdf.add_page_with_borders()

    # Add the headline for the section
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 0, 0)  # Color for the headline
    pdf.cell(0, 10, "Trade Ideas", 0, 1, 'C')
    pdf.ln(10)

    # Helper function to check remaining space and force a page break if needed
    def check_page_break(pdf, required_height):
        if pdf.get_y() + required_height > 270:  # Adjust 270 to avoid breaking too close to the bottom
            pdf.add_page_with_borders()

    # First trade idea
    # Add first image (screenshot from TradingView)
    first_image_path = "C:/Users/strus/Downloads/eu23.png"
    image_width = 120  # Image width in mm
    image_height = 60  # Adjust this based on image dimensions in mm
    x_centered = (210 - image_width) / 2  # Center the image on an A4 page (210mm wide)
    pdf.image(first_image_path, x=x_centered, y=pdf.get_y(), w=image_width)

    # Adjust the paragraph to be closer to the image (reduce space)
    pdf.set_y(pdf.get_y() + image_height + 5)  # Slightly closer to the image

    # First trade explanation
    first_trade_text = (
        "During our Live Trading Session of 23 September at the New York session, we have waited for the neutral US PMI numbers, waiting for a retracement of the price"
        "We took a quick 12 Minutes scalp with a 1:2 RRR." 
        
    )
    # Check if there's enough space for the paragraph
    check_page_break(pdf, required_height=30)  # Estimate 30mm for a 3-4 line paragraph
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, first_trade_text)
    pdf.ln(5)

    # Second trade idea
    # Add second image (screenshot from TradingView)
    second_image_path = "C:/Users/strus/Downloads/gu 23.png"
    pdf.image(second_image_path, x=x_centered, y=pdf.get_y(), w=image_width)

    # Adjust the paragraph to be closer to the second image
    pdf.set_y(pdf.get_y() + image_height + 5)  # Slightly closer to the image

    # Second trade explanation
    second_trade_text = (
        "We got a similar opportunity on the GBPUSD, but we wouldn't take trades having a strong positive correlation for the reason of diversification and capital "
        "conservation, especially that the pair is more volatile during the New york session than the London session."
    )
    # Check if there's enough space for the paragraph
    check_page_break(pdf, required_height=30)  # Estimate 30mm for a 3-4 line paragraph
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, second_trade_text)
    pdf.ln(10)



def fxstreet_fred(pdf):
    # Add a page with border
    pdf.add_page_with_borders()

    # Fetch and process RSS feed
    feed_url = "https://www.fxstreet.com/rss"
    feed = feedparser.parse(feed_url)

    # Add headlines and summaries with separators
    pdf.set_font("Arial", size=12)
    headline_count = 0

    for i, entry in enumerate(feed.entries[:8]):
        title = entry.title
        summary = entry.summary
        url = entry.link

        # Encoding to avoid character issues
        title = title.encode('latin-1', 'ignore').decode('latin-1')
        summary = summary.encode('latin-1', 'ignore').decode('latin-1')

        # Add colored headline
        pdf.set_text_color(149, 110, 38)  # RGB for #c08e32
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, title, ln=True)

        # Reset text color back to black for summary
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 10, summary)
        pdf.ln(5)

        # Add separator line
        pdf.set_draw_color(0, 0, 0)  # Black color for the line
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Horizontal line separator
        pdf.ln(5)

        # Add asterisks pattern instead of icons for visual separation
        pdf.set_font("Arial", size=16)
        pdf.cell(0, 10, "* * * * * * * *", ln=True, align='C')  # Asterisk pattern separator
        pdf.ln(5)

        headline_count += 1

        # After 4 headlines, start a new page
        if headline_count == 4:
            pdf.add_page_with_borders()
            headline_count = 0  # Reset headline count for the next page


    chart_path = "C:/Users/strus/OneDrive/Pictures/Screenshots/pmi us.png"  # Full path to the image

    # Insert the manual Tradeeconomics chart (screenshot)
    pdf.image(chart_path, x=10, y=50, w=190)

    # Adjust the font and format for the interpretation text (same as Personal Analysis)
    pdf.ln(100)  # Add some space after the image (adjust as needed)
    pdf.set_font('Arial', 'B', 16)  # Bold and 16 size for the title
    pdf.cell(0, 10, 'Interpretation of the Data', 0, 1, 'C')  # Center the title
    pdf.ln(10)  # Line break for spacing
    pdf.set_font('Arial', '', 12)  # Regular 12 size for the body text

    # Interpretation Text (You can modify this if needed)
    interpretation_text = (
        "The US Service PMI is a monthly indicator that measures the growth rate of the service sector." 
        "A PMI above 50 suggests expansion, while a PMI below 50 indicates contraction. Given the recent interest rate cut to 5%," 
        "we can expect a positive impact on the service sector as businesses may be more inclined to invest and hire. However," 
        "the actual impact will depend on factors such as the magnitude of the rate cut, overall economic conditions, and other external influences." 
        "To provide a more accurate analysis, it would be helpful to examine the specific PMI values for the relevant months and compare them to historical trends."
    )
    pdf.multi_cell(0, 10, interpretation_text)

def personal_analysis(pdf):
    # Add a page with borders
    pdf.add_page_with_borders()

    # Add a headline for the section
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(0, 0, 0)  # Color for the headline
    pdf.cell(0, 10, "Personal Analysis - Dollar Index (DXY)", 0, 1, 'C')
    pdf.ln(10)

    # Add image (DXY analysis screenshot from TradingView)
    image_path = "C:/Users/strus/Downloads/dxy 23.png"
    pdf.image(image_path, x=(pdf.w - 120) / 2, w=120, h=0, type='PNG')  # Slightly larger image

    # Add the personal analysis text
    personal_analysis_text = (
        "The provided chart depicts the US Dollar Index (DXY) from mid-August to late September 2024." 
        "The Federal Reserve's dovish stance, coupled with Jerome Powell's announcement of a potential interest rate cut," 
        "led to a decline in the dollar. However, stronger-than-expected Non-Farm Payroll numbers temporarily halted the downward trend." 
        "Despite positive NFP data, a neutral US PMI limited the dollar's upward momentum, indicating a complex interplay between economic indicators and" 
        "the currency's value."
    )
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, personal_analysis_text)
    pdf.ln(10)


def generate_report():
    logo_path ='C:/Users/strus/OneDrive/Desktop/TL Logo.png'

    pdf = PDF(logo_path)

    # Table of contents
    table_of_contents(pdf)

    # Sections
    economic_calendar(pdf)
    personal_analysis(pdf)
    trade_ideas(pdf)
    fxstreet_fred(pdf)

    # Save the PDF
    pdf.output("22_november_Report.pdf")


generate_report()

