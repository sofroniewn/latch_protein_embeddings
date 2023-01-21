from pathlib import Path
import pandas as pd
import torch
import esm
from latch.types import LatchDir
from latch import small_gpu_task


TOKS_PER_BATCH = 4096
TRUNCATION_SEQ_LENGTH = 1024
REPR_LAYERS = 6
PER_TOK = False
MEAN = True
BOS = False

@small_gpu_task
def extract_embeddings_from_sequences(sequences: pd.DataFrame, output_dir: LatchDir) -> LatchDir:

    # subset sequences    
    sequences = sequences[:100]

    # Resolve local output dir
    local_output_dir = Path(output_dir).resolve()
    
    # Create dataset
    dataset = esm.data.FastaBatchedDataset(sequences['protein_id'], sequences['protein_sequence'])

    # Load ESM-2 model
    model, alphabet = esm.pretrained.esm2_t6_8M_UR50D()
    model.eval()  # disables dropout for deterministic results

    # Create dataloader
    batches = dataset.get_batch_indices(TOKS_PER_BATCH, extra_toks_per_seq=1)
    data_loader = torch.utils.data.DataLoader(
        dataset, collate_fn=alphabet.get_batch_converter(TRUNCATION_SEQ_LENGTH), batch_sampler=batches
    )

    # Evaluate model
    with torch.no_grad():
        for batch_idx, (labels, strs, toks) in enumerate(data_loader):
            print(
                f"Processing {batch_idx + 1} of {len(batches)} batches ({toks.size(0)} sequences)"
            )
            if torch.cuda.is_available():
                toks = toks.to(device="cuda", non_blocking=True)

            out = model(toks, repr_layers=[REPR_LAYERS], return_contacts=False)

            representations = {
                layer: t.to(device="cpu") for layer, t in out["representations"].items()
            }

            # Save data for each protein individually
            for i, label in enumerate(labels):
                    output_file = local_output_dir / f"{label}.pt"
                    # args.output_file.parent.mkdir(parents=True, exist_ok=True)
                    result = {"label": label}
                    truncate_len = min(TRUNCATION_SEQ_LENGTH, len(strs[i]))
                    # Call clone on tensors to ensure tensors are not views into a larger representation
                    # See https://github.com/pytorch/pytorch/issues/1995
                    if PER_TOK:
                        result["representations"] = {
                            layer: t[i, 1 : truncate_len + 1].clone()
                            for layer, t in representations.items()
                        }
                    if MEAN:
                        result["mean_representations"] = {
                            layer: t[i, 1 : truncate_len + 1].mean(0).clone()
                            for layer, t in representations.items()
                        }
                    if BOS:
                        result["bos_representations"] = {
                            layer: t[i, 0].clone() for layer, t in representations.items()
                        }

                    torch.save(
                        result,
                        output_file,
                    )
    # Return directory
    return LatchDir(local_output_dir, output_dir.remote_path)