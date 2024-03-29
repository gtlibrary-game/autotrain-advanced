# Load necessary libraries
#install.packages("ggplot2")
#install.packages("tidyr")
#install.packages("syuzhet")

library(ggplot2)
library(tidyr)
library(syuzhet)


file_path <- "babbage.csv"

# Load the data
data <- read.csv(file_path, header = FALSE, col.names = c("sent", "speed", "conflict"))
data


sv_data_sent <- as.numeric(data$sent[2:length(data$sent)])
sv_data_sent

plot(sv_data_sent)
simple_plot(sv_data_sent, title = "Narrative")

ft_values <- get_dct_transform(
  sv_data_sent, 
  low_pass_size = 3, 
  x_reverse_len = 100,
  padding_factor = 2,
  scale_vals = TRUE,
  scale_range = FALSE
)

plot(
  ft_values, 
  type ="l", 
  main ="Transformed Values", 
  xlab = "Narrative Time", 
  ylab = "Emotional Valence", 
  col = "red"
)



conflict_data_sent <- as.numeric(data$conflict[2:length(data$conflict)])
conflict_data_sent

plot(conflict_data_sent)
simple_plot(conflict_data_sent, title = "Conflict")

ft_values_conflict <- get_dct_transform(
  conflict_data_sent, 
  low_pass_size = 3, 
  x_reverse_len = 100,
  padding_factor = 2,
  scale_vals = TRUE,
  scale_range = FALSE
)

plot(
  ft_values_conflict, 
  type ="l", 
  main ="Transformed Values", 
  xlab = "Narrative Time", 
  ylab = "Emotional Valence", 
  col = "blue"
)


pace_data_sent <- as.numeric(data$speed[2:length(data$speed)])
pace_data_sent

plot(pace_data_sent)
simple_plot(pace_data_sent, "Pacing")

ft_values_pace <- get_dct_transform(
  pace_data_sent, 
  low_pass_size = 3, 
  x_reverse_len = 100,
  padding_factor = 2,
  scale_vals = TRUE,
  scale_range = FALSE
)

plot(
  ft_values_pace, 
  type ="l", 
  main ="Transformed Values", 
  xlab = "Narrative Time", 
  ylab = "Emotional Valence", 
  col = "green"
)



# Assuming the 'syuzhet' package has already been used to calculate ft_values, ft_values_conflict, and ft_values_pace
# Combine the transformed values into a single data frame for plotting
df <- data.frame(
  Time = 1:length(ft_values),
  Sentiment = ft_values,
  Conflict = ft_values_conflict,
  Pace = ft_values_pace
)

# Melt the data frame to long format for ggplot
df_long <- tidyr::pivot_longer(df, -Time, names_to = "Category", values_to = "Value")

# Plot using ggplot
p <- ggplot(df_long, aes(x = Time, y = Value, color = Category)) +
  geom_line() +
  theme_minimal() +
  labs(title = "Narrative Analysis", x = "Narrative Time", y = "Transformed Value") +
  scale_color_manual(values = c("Sentiment" = "red", "Conflict" = "blue", "Pace" = "green"))

print(p)

# Save the plot to disk
ggsave("babbage.png", plot = p, width = 10, height = 6, dpi = 300)


