FROM node:20

WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# Expose port 8000 for Vite
EXPOSE 8000

# Start the Vite development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]