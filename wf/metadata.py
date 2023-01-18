from latch.types import LatchAuthor, LatchMetadata, LatchParameter


metadata = LatchMetadata(
    display_name="Extract embeddings for all protein sequences",
    author=LatchAuthor(
        name="Nicholas Sofroniew",
        email="sofroniewn@gmail.com",
        github="github.com/sofroniewn",
    ),
    # repository="https://github.com/your-repo",
    license="MIT",
    parameters={
        "output_dir": LatchParameter(
            display_name="Output directory",
            description="Location to save embeddings too",
            batch_table_column=True,  # Show this parameter in batched mode.
        ),
    },
    tags=[],
)