def hanoi_iterative(n, source='A', target='C', auxiliary='B'):
    moves = []
    # Explicit call stack storing frame tuples: (disks, source, target, auxiliary)
    stack = [(n, source, target, auxiliary)]
    
    while stack:
        disks, src, tgt, aux = stack.pop()
        if disks == 1:
            moves.append((src, tgt))
        elif disks > 1:
            # Push calls in reverse execution order (LIFO stack)
            stack.append((disks - 1, aux, tgt, src))  # Step 3
            stack.append((1, src, tgt, aux))           # Step 2
            stack.append((disks - 1, src, aux, tgt))  # Step 1
            
    return moves

# Example usage
print("Iterative Hanoi (3 disks):", hanoi_iterative(3))