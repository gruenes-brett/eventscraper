from eventscraper.scrapers.applicationldjsonscraper import ApplicationLdJsonScraper


def test_convert_numbers_to_strings_in_json():
    replaced = ApplicationLdJsonScraper.convert_numbers_to_strings_in_json('''
    {
        "upsi": 01234,
        "dupsi": 
            1234 ,
        "notme": "333",
        "nope": "3:33",
        "yes" :   444
    }
    ''')

    assert '''
    {
        "upsi": "01234",
        "dupsi": 
            "1234" ,
        "notme": "333",
        "nope": "3:33",
        "yes" :   "444"
    }
    ''' == replaced

def test_clean_invalid_json():
    cleaned = ApplicationLdJsonScraper.clean_invalid_json('''
    {
        "some": "where",
        "over": "the rainbow",
        
        <!----><!----><!---->  }
    ''')

    assert '''
    {
        "some": "where",
        "over": "the rainbow",
        
          }
    ''' == cleaned


def test_drop_invalid_lines():
    cleaned = ApplicationLdJsonScraper.drop_invalid_lines('''
    {
        "some": "where",
        "over": "the "rainbow"",
        "way": "up high"
    }
    ''')

    assert '''
    {
        "some": "where",
        "way": "up high"
    }
    ''' == cleaned


def test_remove_superfluous_commata():
    cleaned = ApplicationLdJsonScraper.remove_superfluous_commata('''
    {
        "some": "where",
        "over": {
            "the": "rainbow",
        },
    }
    ''')

    assert '''
    {
        "some": "where",
        "over": {
            "the": "rainbow" } }
    ''' == cleaned


def test_fix_timezone():
    data = {}
    data['mydate1'] = '2022-03-28T23:11:00+00:00'
    data['mydate2'] = '2022-03-28T13:11:00+00:00'
    data['mydate3'] = '2022-03-28T00:11:00+00:00'
    data['badformat'] = 'asdf'

    ApplicationLdJsonScraper.fix_timezone(data, 'mydate1')
    assert '2022-03-29T01:11' == data['mydate1']

    ApplicationLdJsonScraper.fix_timezone(data, 'mydate2')
    assert '2022-03-28T15:11' == data['mydate2']

    ApplicationLdJsonScraper.fix_timezone(data, 'mydate3')
    assert '2022-03-28T02:11' == data['mydate3']

    # expect no error
    ApplicationLdJsonScraper.fix_timezone(data, 'no_key')
    ApplicationLdJsonScraper.fix_timezone(data, 'badformat')
