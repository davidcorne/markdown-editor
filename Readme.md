# Markdown Editor

## Building

### Docker

Docker is the easiest way to build this. The commands are:

1. **Build container:** `docker build -t mde -f .\.devcontainer\Dockerfile .`
2. **Run container:** `docker run -it mde`

To debug the Dockerfile, you want to do something like: `docker run -it -v <development-location>\markdown-editor:/mde mde bash`.
