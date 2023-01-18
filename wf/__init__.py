"""
Generate Protein Embeddings based on Ensemble IDs / 
"""

from latch import workflow
from latch.resources.launch_plan import LaunchPlan
from latch.types import LatchOutputDir
from .sequences import get_all_protein_sequences
from .embeddings import extract_embeddings_from_sequences
from .metadata import metadata


@workflow(metadata)
def extract_embeddings(output_dir: LatchOutputDir) -> LatchOutputDir:
    """Extract Protein Embeddings From Sequences

    markdown header
    ----

    Use EMSv2 to extract protein embeddings from all proteins with an Ensmbl Id.
    """
    sequences = get_all_protein_sequences()
    return extract_embeddings_from_sequences(sequences=sequences, output_dir=output_dir)


"""
Add test data with a LaunchPlan. Provide default values in a dictionary with
the parameter names as the keys. These default values will be available under
the 'Test Data' dropdown at console.latch.bio.
"""
LaunchPlan(
    extract_embeddings,
    "Test Data",
    {
        "output_dir": LatchOutputDir("latch:///sofroniewn/protein-embeddings/esmv2/test_1/"),
    },
)