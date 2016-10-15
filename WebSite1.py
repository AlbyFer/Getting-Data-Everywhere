

doc = '/Users/StarShipIV/Documents/Progetti/Source/Foo.rtf'

def Foo_results(path, save = True): # Adjust name of file with result
    import urllib
    from bs4 import BeautifulSoup
    import pandas as pd

    def res_other_blocks(url):

        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)

        div = BeautifulSoup(str(soup('div', id='cpm')))
        script_day = BeautifulSoup(str(div('script')))
        day = str(script_day.get_text())[41:51]  # For the day of the race

        blocks_soup = soup.find_all('div', class_='crBlock ')

        res_day = pd.DataFrame(columns=['Horse', 'Position', 'Day', 'Time', 'Track'])

        for i in range(len(blocks_soup)):

            blocks = BeautifulSoup(str(blocks_soup[i]))

            td = BeautifulSoup(str(blocks.find_all('td')[1]))
            cond = BeautifulSoup(str(blocks.find_all('a')[1])).get_text()

            if len(cond) == 0:
                venue = td.get_text().split(' ')[3]  # For the name of the track
            else:
                venue = cond

            table = BeautifulSoup(str(blocks.find_all('table', class_='resultGrid')))

            res_block = pd.DataFrame(columns=['Horse', 'Position', 'Day', 'Time', 'Track'])

            tr_soup = table.find_all('tr')

            for k in range(0, len(tr_soup), 2):

                tr = BeautifulSoup(str(tr_soup[k]))

                res_tr = pd.DataFrame(columns=['Horse', 'Position', 'Day', 'Time', 'Track'])

                td_soup = tr.find_all('td')
                for h in range(len(td_soup)):
                    if str(td_soup[h]) == '<td>\\xa0</td>
                        td_soup[h] = None

                td_soup = filter(None, td_soup)

                for j in range(len(td_soup)):
                    res_td = pd.DataFrame(columns=['Horse', 'Position', 'Day', 'Time', 'Track'])

                    td1 = BeautifulSoup(str(td_soup[j]))
                    strong_hour = BeautifulSoup(str(td1.strong))
                    hour = strong_hour.get_text()  # For the time of the race

                    p = BeautifulSoup(str(td1.find_all('p')[1]))
                    a_horses = BeautifulSoup(str(p.find_all('a')))
                    horses0 = str(a_horses.get_text()).replace('[', '').replace(']', '').replace("'",
                                                                                                 '')  # For the names of the horses
                    horses = horses0.split(',')

                    pos = range(1, len(horses) + 1)
                    time = [hour] * len(horses)
                    track = [venue] * len(horses)

                    res_td.Horse = horses
                    res_td.Position = pos
                    res_td.Time = time
                    res_td.Track = track
                    res_td.Day = day

                    res_tr = pd.concat([res_tr, res_td], ignore_index=True)

                res_block = pd.concat([res_block, res_tr], ignore_index=True)

            res_day = pd.concat([res_day, res_block], ignore_index=True)
        return (res_day)

    def res_first_block(url):

        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)

        div = BeautifulSoup(str(soup('div', id='cpm')))
        script_day = BeautifulSoup(str(div('script')))
        day = str(script_day.get_text())[41:51]

        first_block_soup = soup.find_all('div', class_='crBlock noBorder')
        blocks = BeautifulSoup(str(first_block_soup))

        td = BeautifulSoup(str(blocks.find_all('td')[1]))
        cond = BeautifulSoup(str(blocks.find_all('a')[1])).get_text()

        if len(cond) == 0:
            venue = td.get_text().split(' ')[3]  # For the name of the track
        else:
            venue = cond

        table = BeautifulSoup(str(blocks.find_all('table', class_='resultGrid')))

        res_block1 = pd.DataFrame(columns=['Horse', 'Position', 'Day', 'Time', 'Track'])

        tr_soup = table.find_all('tr')

        for k in range(0, len(tr_soup), 2):

            tr = BeautifulSoup(str(tr_soup[k]))

            res_tr = pd.DataFrame(columns=['Horse', 'Position', 'Day', 'Time', 'Track'])

            td_soup = tr.find_all('td')
            for h in range(len(td_soup)):
                if str(td_soup[h]) == '<td>\\\\xa0</td>':
                    td_soup[h] = None

            td_soup = filter(None, td_soup)

            for j in range(len(td_soup)):
                res_td = pd.DataFrame(columns=['Horse', 'Position', 'Day', 'Time', 'Track'])

                td1 = BeautifulSoup(str(td_soup[j]))
                strong_hour = BeautifulSoup(str(td1.strong))
                hour = strong_hour.get_text()  # For the time of the race

                p = BeautifulSoup(str(td1.find_all('p')[1]))
                a_horses = BeautifulSoup(str(p.find_all('a')))
                horses0 = str(a_horses.get_text()).replace('[', '').replace(']', '').replace("'",
                                                                                             '')  # For the names of the horses
                horses = horses0.split(',')

                pos = range(1, len(horses) + 1)
                time = [hour] * len(horses)
                track = [venue] * len(horses)

                res_td.Horse = horses
                res_td.Position = pos
                res_td.Time = time
                res_td.Track = track
                res_td.Day = day

                res_tr = pd.concat([res_tr, res_td], ignore_index=True)

            res_block1 = pd.concat([res_block1, res_tr], ignore_index=True)
        return (res_block1)

    first_block = res_first_block(path)
    other_blocks = res_other_blocks(path)

    final = pd.concat([first_block, other_blocks], ignore_index=True)

    if save == True:
        final.to_csv('/Users/StarShipIV/Documents/Progetti/Results/3_res')
    return(final)


test = Foo_results(doc)

