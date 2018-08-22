DOCKER_REPO_NAME ?=
DOCKER_CONTAINER_NAME ?= fundamental-analysis
DOCKER_IMAGE_NAME ?= ${DOCKER_REPO_NAME}${DOCKER_CONTAINER_NAME}

# Build the Docker image for this project
build:
	docker-compose build

# Run the services associated with the application
run:
	docker-compose up

# Recreate the database (THIS WILL DELETE ALL EXISTING DATA)
recreate:
	docker-compose -f docker-compose.yml \
  run app python manage.py recreate_db

# Run the flask unit tests
test:
	docker-compose -f docker-compose.yml \
  run app python manage.py test

# Seed the database with S&P 500 stocks
seed:
	docker-compose -f docker-compose.yml \
  run app python manage.py seed_db

# Calculate MOS & Sticker Price
calc:
	docker-compose -f docker-compose.yml \
  run app python manage.py get_mos
# Stop all services associated with the application
down:
	docker-compose down
