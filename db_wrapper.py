import asyncio
import inspect
import functools
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_session():
    print("get_session before")
    yield 100
    print("get_session after")


def get_db(name: str = "db"):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            signature = inspect.signature(func)
            bound_arguments = signature.bind_partial(*args, **kwargs)
            bound_arguments.apply_defaults()

            if name not in bound_arguments.arguments:
                async with get_session() as session:
                    kwargs[name] = session
                    return await func(*args, **kwargs)
            else:
                return await func(*args, **kwargs)

        return wrapped

    return wrapper


@get_db()
async def save(data: str, db: int):
    print("Data", data)
    print("DB", db)


async def main():
    await save("test 1", 10)
    print("=" * 64)
    await save("test 2", db=10)
    print("=" * 64)
    await save("test 3")


asyncio.run(main())
