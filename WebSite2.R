# --------------------------------------------------------------------------------------------------------------- #

# Horse racing results scraping on Foo.com
# Alberto Ferrando

# --------------------------------------------------------------------------------------------------------------- #

get_results_foo <- function(path_to_save){
  
  # Function that scrapes the foo sportbook, collects the horses odds and returns the results both as
  # a DataFrame and as a .csv file saved in the folder provided by the user through path_to_save. The function 
  # always returns the odds for the race day after the day of scraping (e.g. if it's Monday, the function will
  # return the odds for Tuesday)
  #
  # Inputs: path_to_save - a string defining the folder where to save the .csv file with the data
  # Outputs: a dataframe with columns: Horse | Odds | Track | Time | Day | Date + Time of scraping.
  #          It will also such dataframe as a .csv file in the folder give. The name of the file will
  #          be 'foo_Results_' followed by the date and time of scraping
  
  
  library('magrittr')
  library('rvest')
  library('stringr')
  library('lubridate')
  
  day <- gsub('-', '', as.Date(Sys.Date()) + 1)
  
  html <- paste('https://foo.com', day, '&modules=multipick-horse-racing', sep = '')
  foo_results <- read_html(html)
  
  
  # Get the horses
  nodes_horses <- html_nodes(foo_results, xpath = '//div[@class="runner-horse-cell"]')
  horses <- html_text(nodes_horses)
  horses <- str_replace_all(horses, '\n', '')
  
  # Get the odds: to convert to decimals! Separate num and den by '/'
  nodes_odds <- html_nodes(foo_results, xpath = '//li[@class="race-data-item"]')
  odds_temp <- html_text(nodes_odds) 
  odds_temp <- sub('\n ', '', odds_temp)
  odds_temp <- str_replace_all(odds_temp, ' ', '')
  
  odds <- matrix(ncol = 1, nrow = length(odds_temp))
  for (i in 1:length(odds_temp)) {
    if (odds_temp[i] == 'SP') {
      odds[i] == 'SP'
    } else {
      num_den <- suppressWarnings(as.numeric(unlist(strsplit(odds_temp[i], '/'))))
      odds[i] <- sum(num_den)/num_den[2]
    }
  }
  
  
  # Get the places, times and number of horses for each race
  nodes_places_times <- html_nodes(foo_results, xpath = '//div[@class="race-top-info"]')
  places_times <- html_text(nodes_places_times) # For some weird reason the site only allows to see up to a certain hour. This happens even in the source code.
  places_times <- sub(' Runners', '', places_times)
  places_times <- unlist(strsplit(places_times, " (?!.* )", perl = TRUE))
  places_times <- unlist(regmatches(places_times, regexpr(" ", places_times), invert = TRUE))
  
  
  index_times <- seq(from= 1, to= length(places_times), by=3)
  index_places <- seq(from= 2, to= length(places_times), by=3)
  index_runners <- seq(from= 3, to= length(places_times), by=3)
  hours <- places_times[index_times]
  places <- places_times[index_places]
  runners <- as.integer(places_times[index_runners]) # Needed to replicate the venues and times
  
  venues <- c()
  times <- c()
  for (i in 1:length(runners)) {
    interm <- replicate(runners[i], places[i])
    venues <- append(venues, interm)
    interm2 <- replicate(runners[i], hours[i])
    times <- append(times, interm2)
  } # Loop needed to replicate the values the correct number of runners
  
  date_scrp <- rep(Sys.time(), length(horses))
  date_run <- rep(as.Date(as.character(day),  format="%Y%m%d"), length(horses))
  results <- data.frame(matrix(ncol= 6, nrow= length(horses)))
  colnames(results) <- c('Horse', 'Odds', 'Track', 'Time', 'Day', 'Date of scraping')
  
  results['Horse'] <- horses
  results['Odds'] <- odds
  results['Track'] <- venues
  results['Time'] <- times
  results['Date of scraping'] <- date_scrp
  results['Day'] <- date_run
  
  day_of_scrap <- Sys.time()
  file_name <- paste('Foo_Results', day_of_scrap, sep = '_')
  path <- paste(path_to_save, file_name, sep = '/')
  write.csv(results, row.names = FALSE, file= path)
  return(results)
}


example <- get_results_foo('/Users/StarShipIV/Documents/Progetti/Results')
