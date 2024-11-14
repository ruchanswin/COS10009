
def intersection(range1, range2)
  if range1.begin < range2.begin
    if range1.end < range2.begin
      # Ranges do not intersect
      return nil
    else
      return (range2.begin..range1.end)
    end
  else
    if range2.end < range1.begin
      # Ranges do not intersect
      return nil
    else
      return (range1.begin..range2.end)
    end
  end
end

p intersection(1..7, 3..9)
p intersection(1..7, 8..9)
p intersection(12..17, 3..9)
p intersection(12..17, 9..14)
