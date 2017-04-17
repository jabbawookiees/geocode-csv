import geocoder
import click
import time
import csv

IGNORED_ADDRESSES = set([])


def load_output_data(outputfile):
    outputfile.seek(0)
    reader = csv.reader(outputfile)
    output_data = {}
    for row in reader:
        key, longitude, latitude, city, country, status, raw_data = row
        output_data[key] = {
            'lng': longitude,
            'lat': latitude,
            'city': city,
            'country': country,
            'status': status,
            'raw': raw_data,
        }
    return output_data


def load_input_data(inputfile):
    reader = csv.reader(inputfile)
    return [row[0] for row in reader]


def geocode(address):
    g = geocoder.google(address)
    if g.ok:
        return {
            'lat': g.json.get('lat'),
            'lng': g.json.get('lng'),
            'city': g.city or '',
            'country': g.country or '',
            'status': 'OK',
            'raw': g.json,
        }
    else:
        raise Exception(g.error)


def empty_data(status='Ignored'):
    return {
        'lat': '',
        'lng': '',
        'city': '',
        'country': '',
        'status': status,
        'raw': '',
    }


@click.command()
@click.argument('inputpath')
@click.option('-o', '--output', default='output.csv')
def main(inputpath, output):
    start_time = time.time()
    inputfile = open(inputpath, 'r')
    outputfile = open(output, 'a+')
    input_data = load_input_data(inputfile)
    output_data = load_output_data(outputfile)
    outputfile.close()
    outputfile = open(output, 'w+')
    output_csv = csv.writer(outputfile)
    for count, address in enumerate(input_data):
        data = None
        if address in IGNORED_ADDRESSES:
            data = empty_data()
        elif address in output_data:
            data = output_data[address]
        else:
            while data is None:
                try:
                    data = geocode(address)
                except Exception, e:
                    if e.message == 'ZERO_RESULTS':
                        data = empty_data(status='No Results')
                    else:
                        print "Failed to get {}. Sleeping...".format(address)
                        time.sleep(3)
        lat = data['lat']
        lng = data['lng']
        city = data['city']
        country = data['country']
        status = data['status']
        raw = data['raw']
        output_csv.writerow([address, lat, lng, city, country, status, raw])
        outputfile.flush()
        elapsed_time = time.time() - start_time
        print 'Progress: {} / {} ({}) -- Last Finished: {}'.format(count, len(input_data), elapsed_time, address)

if __name__ == '__main__':
    main()
