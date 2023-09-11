args <- commandArgs(trailingOnly=TRUE)
output <- args[1]
sink(file=output)
installed.packages()
sink()

