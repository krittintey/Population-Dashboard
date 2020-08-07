# Population Dashboard using Dash (Plotly)

Dockerize a Python Dash app for quick prototyping.

## Switch mode when data is updated

```
ENV UPDATE_DATA True # False
```

## Build and run

```
docker build -t dashboard .
docker run -d -p 8050:8050 dashboard
```

## Access the page

Go to `http://0.0.0.0:8050/` in browser.