# Load the required library
library("pheatmap")

# Get the input file name from command-line arguments
args <- commandArgs(trailingOnly = TRUE)

# Set default input file if no arguments are provided
input_file <- ifelse(length(args) >= 1, args[1], "matrix.txt")

# Read in the input file as a matrix
data <- as.matrix(read.table(input_file, header = TRUE, row.names = 1))

# Save image
png(filename = "heatmap.png", width = 1000, height = 1000,
    units = "px", pointsize = 12, bg = "white", res = NA)

# Create the heatmap with row and column labels
pheatmap(data)

# Close the graphics device
dev.off()
