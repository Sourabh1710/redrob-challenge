import json
import csv
import time
from src.ranking_engine import calculate_composite_score

def run_ranking(input_path, output_path):
    print("Starting candidate evaluation pipeline...")
    start_time = time.time()
    
    scored_candidates = []
    
    with open(input_path, "r", encoding="utf-8") as f:
        # Loop through all 100,000 lines
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue

            # Parse candidate JSON    
            candidate = json.loads(line)
            candidate_id = candidate.get("candidate_id")
            
            # Calculate final composite score
            score, reasoning = calculate_composite_score(candidate)
            
            # Save only the minimum required info to conserve memory
            scored_candidates.append({
                "candidate_id": candidate_id,
                "score": score,
                "reasoning": reasoning
            })
            
            # Print progress update every 20,000 lines
            if line_num % 20000 == 0:
                print(f"Processed {line_num} candidates...")


    # Sorted 'scored_candidates' 
    #    - Primary key: score (descending)
    #    - Secondary key: candidate_id (ascending, for deterministic tie-breaking)
    scored_candidates.sort(key=lambda x: (-x["score"], x["candidate_id"]))
    
    # Sliced the top 100 sorted candidates
    top_100_candidates = scored_candidates[:100]
    
    with open(output_path, "w", encoding="utf-8", newline="") as csv_file:
        
        writer = csv.writer(csv_file)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        
        for rank, candidate in enumerate(top_100_candidates, start=1):
            writer.writerow([
                candidate["candidate_id"],
                rank,
                candidate["score"],
                candidate["reasoning"]
            ])
    
    elapsed = time.time() - start_time
    print(f"Ranking complete! Output saved to {output_path}")
    print(f"Total execution time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    run_ranking("data/candidates.jsonl", "data/submission.csv")