# SA.:Phase 4 Code Challenge: Late Show API

## Project Overview

This code challenge is a chance for you to show off how much you've learned specifically about; models, relationships, and validations, routes and REST, and response structure. 

## Features

- **Episodes Management:** Retrieve all episodes, view episode details, create new episodes, and delete episodes.
- **Guests Management:** Retrieve the list of guests and their details.
- **Appearances Management:** Create new appearances linking episodes and guests, with a rating system.
- **Error Handling:** Custom error responses with detailed validation errors.
- **Database Migrations:** Easily update the database schema using Flask-Migrate.

## Technologies Used

- ***Python 3.x***
- ***Flask:*** Web framework for building RESTful APIs.
- ***SQLAlchemy:*** ORM used for database interactions.
-***SQLite:*** Database for local development and testing.
- ***Flask-Migrate:*** For handling database migrations.
- ***Marshmallow:*** (Optional) for data validation and serialization.

## Topics Covered

1. **SQLAlchemy Migrations:**

- `Flask-Migrate` is utilized to manage and apply database schema changes, such as adding or altering tables and columns, ensuring smooth transitions as the database evolves.

2. **SQLAlchemy Relationships:**

- One-to-Many Relationships are implemented between key models, such as `Episode`,  , and the `Appearance` table, which serves as an association table.
- Bidirectional Relationships between models are handled using `back_populates`, facilitating interactions between related tables, such as `Episode` and `Appearance`, and `Guest` and `Appearance`.
- The `overlaps` attribute is used to avoid ambiguities in SQLAlchemy relationships when two models share a third.

3. **Validation and Error Handling:**

- Input validation is enforced in routes like `/appearances` to ensure that required fields (e.g., `episode_id`, `guest_id`, and `rating`) are properly provided and conform to expected formats or constraints.
- Error messages are returned for missing or invalid fields with specific feedback, such as `"errors": ["Episode ID is required"]` or `"errors": ["Guest not found"]`.

4. **Data Serialization:**

- Data serialization is managed manually in JSON responses to ensure the correct structure and fields are returned in the API responses, especially for endpoints like `/episodes`, `/guests`, and `/appearances`.
- Nested relationships (e.g., between `Appearances`, `Guests`, and `Episodes`) are formatted in custom JSON structures to align with API expectations.

5. **CRUD Operations:**

- GET routes retrieve records, such as listing all episodes (`/episodes`) or fetching a specific guest (`/guests/<id>`).
- POST routes handle creating new records, such as associating a `Guest` with an `Episode` via the `Appearance` model.
- DELETE routes allow for the removal of records, like deleting an `Episode` by its ID.

6. **Error Handling with IntegrityError:**

- Database integrity issues, such as foreign key violations, are managed with `try-except` blocks to ensure graceful error handling during record creation, especially for associations in the `Appearance` model.

7. **Flask Request Handling:**

- Flask's `request.get_json()` is used to extract incoming request payloads for validation and processing. For instance, fields such as `rating`, `guest_id`, and `episode_id` are validated before creating an `Appearance`.

8. **Response Formatting:**

- JSON responses are formatted consistently, and appropriate HTTP status codes are returned (e.g., `201` for successfully created records, `404` for not found errors, `400` for invalid data inputs).

## Schema : Tables

![Models](/models-img)


- An `Episode` has many `Guest`s through `Appearance`
- A `Guest` has many `Episode`s through `Appearance`
- An `Appearance` belongs to a `Guest` and belongs to a `Episode`


## Instructions to run the program:

*Step 1:* **Clone the repository to your preferred directory:**

```txt
git clone git@github.com:code-iddih/phase-04-week-02-code-challenge.git
```

*Step 1:* **Navigate to root directory:**

```txt
cd phase-04-week-02-code-challenge
```

*Step 2:* **Install dependencies (listed in `Pipfile`):**

```txt
pipenv install
```
*Step 3:* **Activate the virtual environment:**

```txt
pipenv shell
```
*Step 4:* **Navigate to Server directory:**

```txt
cd server
```
*Step 5:* **Run the application:**

```txt
python3 app.py
```
*Step 6:* **Test the Routes in the browser or API Platform:**

*Step 6:* **specifically Use API Platform to test for `PATCH` and `POST` routes::**

Downlaod any of them here:\
[postman](https://postman.com)\
[insomnia](https://insomnia.rest/)

## Routes

**1. GET /`episodes`**

- Retrieves a list of all episodes from the database. Each episode is serialized with its `id`, `date`, and `number`.

Expected Output:

```txt
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  },
  {
    "id": 2,
    "date": "1/12/99",
    "number": 2
  }
]
```

**2. GET /`episodes/:id`**

- Fetches the details of a specific episode by its `id`. This includes the episode's `id`, `date`, `number`, and the appearances associated with it. Each appearance includes details about the guest and their rating.

Expected Output:

```txt
{
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1,
    "appearances": [
        {
            "episode_id": 1,
            "guest": {
                "id": 1,
                "name": "Michael J. Fox",
                "occupation": "actor"
            },
            "guest_id": 1,
            "id": 1,
            "rating": 4
        }
    ]
}
```

**3. GET /`guests`**

- Returns a list of all guests from the database. Each guest is serialized with their `id`, `name`, and `occupation`.

Expected Output:

```txt
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  },
  {
    "id": 2,
    "name": "Sandra Bernhard",
    "occupation": "Comedian"
  },
  {
    "id": 3,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
]

```

**4. POST /`appearances`**

- Creates a new `Appearance` linking an existing episode and guest. The request accepts `rating`, `episode_id`, and `guest_id`, and if successful, returns the newly created appearance data along with the related episode and guest details.

Expected response Format:

```txt
{
  "rating": 5,
  "episode_id": 1,
  "guest_id": 3
}
```

Expected Output:

```txt
{
  "id": 162,
  "rating": 5,
  "guest_id": 3,
  "episode_id": 2,
  "episode": {
    "date": "1/12/99",
    "id": 2,
    "number": 2
  },
  "guest": {
    "id": 3,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
}
```

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



