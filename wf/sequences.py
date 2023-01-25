from latch import small_task
from pyensembl import EnsemblRelease
import pandas as pd


@small_task
def get_protein_sequence_from_protein_id(protein_id: str) -> str:
    genome = EnsemblRelease(77)
    return genome.protein_sequence(protein_id)


@small_task
def get_all_protein_sequences() -> pd.DataFrame:
    genome = EnsemblRelease(77)
    results = []
    for protein_id in genome.protein_ids():
        sequence = genome.protein_sequence(protein_id)
        if '*' not in sequence:
            results.append({
                'protein_id': protein_id,
                'protein_sequence': sequence
            }) 
    return pd.DataFrame(results)