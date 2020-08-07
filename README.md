# Population Dashboard using Dash (Plotly)

## Switch mode when data is updated

```
ENV UPDATE_DATA True # False
```

## Build and run

```
docker build -t dashboard .
docker run --rm -p 8050:8050 dashboard
(When you want to update the models)
docker run --rm --env UPDATE_DATA=True -p 8050:8050 dashboard
```

## Access the page

Go to `http://0.0.0.0:8050/` or `http://localhost:8050/` in browser.
