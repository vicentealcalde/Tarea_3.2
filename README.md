# Assignment 3 Base

## Database

You can fill the 3 tables (Authors, Books, Ratings) from the 3 csv files in the `database_files` folder.

## Commands

### Start dev environment
```bash
docker-compose up --build
```

### Run in production
```bash
docker-compose -f docker-compose.prod.yml up --build
```

### Create Migrations
```bash
flask --app books db revision '<MESSAGE>'
```

### Run Migrations
```bash
flask --app books db upgrade
```
