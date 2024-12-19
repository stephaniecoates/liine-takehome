# liine-takehome

Technical takehome assignment instructions can be found here: https://gist.github.com/sharpmoose/d25487b913a08f6a6e6059c07035a041

### API endpoint
`GET /open-restaurants`

##### Query Parameters:
| Parameter   | Type     | Required | Description                            | Example           |
|-------------|----------|----------|----------------------------------------|-------------------|
| `datetime`  | `string` | Yes      | The date and time to check in format `YYYY-MM-DD HH:MM` | `2024-12-20 13:00` |

##### Response
The endpoint returns a JSON object with the following structure:

| Field              | Type              | Description                                              |
|---------------------|-------------------|----------------------------------------------------------|
| `open_restaurants` | `array of strings` | A list of restaurant names that are open at the date and time specified in the query parameter. |
