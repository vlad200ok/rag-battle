
files="
-f docker-compose.yml
-f docker/docker-compose.yml
-f docker/docker-compose-override.yml
"

processed_build_args=()
for arg in "$@"; do
  if [ "$arg" != "-d" ]; then
    processed_build_args+=("$arg")
  fi
done

docker compose $files build --parallel "${processed_build_args[@]}"
docker compose $files up "$@"