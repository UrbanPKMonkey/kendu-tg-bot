# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files from your project into the container
COPY . .

# Install all required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Railway uses (can be dynamically assigned)
EXPOSE 80

# Command to run your bot
CMD ["python3", "bot.py"]
