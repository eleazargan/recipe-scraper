FROM node:12.2.0-alpine

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY ./web/ /app/

# Disable for now. Run npm install on server

# RUN npm install --silent
# RUN npm install react-scripts@3.0.1 -g --silent

# start app
CMD ["npm", "start"]