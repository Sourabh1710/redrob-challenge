import json
import csv
import time
import heapq
import logging
from src.ranking_engine import calculate_composite_score

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Custom Heap Element to manage scores and alphabetical ID tie-breaking
class CandidateHeapElement:
    def __init__(self, score, candidate_id, reasoning):
        self.score = score
        self.candidate_id = candidate_id
        self.reasoning = reasoning

    def __lt__(self, other):
        # Primary comparison: Score (higher score is better)
        if self.score != other.score:
            return self.score < other.score
            
        # Secondary comparison: Candidate ID (smaller alphabetical ID is better)
        # Because this is a min-heap (popping the "smallest" elements), so, I reverse
        # the comparison for IDs. The LARGER ID string is treated as less valuable.
        return self.candidate_id > other.candidate_id

def run_ranking(candidates_path, output_path):
    logger.info("Initializing candidate ranking pipeline.")
    start_time = time.time()
    
    # Initialize the min-heap
    top_candidates_heap = []
    processed_count = 0
    
    with open(candidates_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
                
            candidate = json.loads(line)
            candidate_id = candidate.get("candidate_id")
            score, reasoning = calculate_composite_score(candidate)
            
            # Wrap the candidate details in the custom heap element
            element = CandidateHeapElement(score, candidate_id, reasoning)
            
            # Push into heap and keep heap size capped at exactly 100
            heapq.heappush(top_candidates_heap, element)
            if len(top_candidates_heap) > 100:
                heapq.heappop(top_candidates_heap)
                
            processed_count += 1
            if processed_count % 20000 == 0:
                logger.info(f"Successfully processed {processed_count} candidates.")

    # Extract and sort the final 100 candidates from the heap (descending)
    sorted_top_100 = []
    while top_candidates_heap:
        sorted_top_100.append(heapq.heappop(top_candidates_heap))
    
    # Since heappop returns elements smallest-first, I reverse the list to get descending order
    sorted_top_100.reverse()
    
    # Write results to output path
    logger.info(f"Writing top 100 ranked candidates to {output_path}")
    with open(output_path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        
        for rank, element in enumerate(sorted_top_100, start=1):
            writer.writerow([
                element.candidate_id,
                rank,
                element.score,
                element.reasoning
            ])
            
    elapsed = time.time() - start_time
    logger.info(f"Pipeline complete! Output saved to {output_path}")
    logger.info(f"Execution profile: Processed {processed_count} records in {elapsed:.2f} seconds.")

if __name__ == "__main__":
    run_ranking("data/candidates.jsonl", "data/submission.csv")