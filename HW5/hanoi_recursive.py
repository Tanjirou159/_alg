def hanoi_recursive(n, source='A', target='C', auxiliary='B'):
    moves = []
    
    def _hanoi(disks, src, tgt, aux):
        if disks > 0:
            # Step 1: Move n-1 disks from src to aux
            _hanoi(disks - 1, src, aux, tgt)
            # Step 2: Move the largest disk to tgt
            moves.append((src, tgt))
            # Step 3: Move n-1 disks from aux to tgt
            _hanoi(disks - 1, aux, tgt, src)
            
    _hanoi(n, source, target, auxiliary)
    return moves

# Example usage
print("Recursive Hanoi (3 disks):", hanoi_recursive(3))