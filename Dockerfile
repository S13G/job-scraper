FROM python:3.9-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create a folder for the app
WORKDIR /scraper

# Copy the requirements.txt file into the workdir
COPY requirements.txt ./

# Install the dependencies
RUN pip3 install -r requirements.txt

# Copy the entire project into the workdir
COPY . /scraper

# Run the scraper
CMD ["python3", "run.py"]