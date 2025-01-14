from fuzzywuzzy import fuzz
from datetime import datetime, timedelta,timezone
import nltk
from nltk.corpus import stopwords,wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from lms.models import Book, Rating


if not nltk.download('punkt', quiet=True):
    nltk.data.find('tokenizers/punkt')


try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords', quiet=True)


try:
    wordnet.synsets('dog')
except LookupError:
    nltk.download('wordnet', quiet=True)

def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text.lower())  

    
    tokens = [token for token in tokens if token.isalpha()]

    
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return ' '.join(lemmatized_tokens)





def split_strings_into_chunks(strings, x):
    result = []
    for string in strings:
        words = string.split()  
        for i in range(0, len(words), x):  
            result.append(' '.join(words[i:i+x]))  
    return result


def fuzzy_search(query, threshold=40):
    
    books = Book.query.filter_by(is_available=True).all()

    query = lemmatize_text(query)
    q_len = len(query.split(" "))

    results = []

    total_time = 0
    for book in books:                
        name_chunks = split_strings_into_chunks([lemmatize_text(book.book_name)],q_len)
        if len(name_chunks) == 0:
            continue


        name_scores = [fuzz.ratio(query, chunk) for chunk in name_chunks]
        max_name_score = max(name_scores)

        if max_name_score >= 40:
            results.append((book, max_name_score))

            continue

        author_names = [lemmatize_text(author.author_name) for author in book.authors.all()]
 
        author_chunks = split_strings_into_chunks(author_names,q_len)
        if len(author_chunks)== 0:
            continue

        author_scores = [fuzz.ratio(query, chunk) for chunk in author_chunks]
        max_author_score = max(author_scores)

        if max_author_score >= 40:
            results.append((book, max_author_score))

            continue

        
        section_score = fuzz.ratio(query,lemmatize_text(book.section.section_name))

        if section_score >= 40:
            results.append((book, section_score))

            continue

        text_chunks = split_strings_into_chunks([book.preprocessed_text],q_len)
        if len(text_chunks)== 0:
            continue
        

            
        text_scores = [fuzz.ratio(query, chunk) for chunk in text_chunks]
        max_text_score = max(text_scores)

        if max_text_score >= 60:
            results.append((book, max_text_score))

    results = sorted(results,key = lambda x:x[1],reverse=True)
    results = [result[0].book_id for result in results]
    return results



def report_content(user):
    content = {
        "total_spending":0,
        "full_name":user.username,
        "collection":[]
    }
    cut_off = datetime.now(timezone.utc)-timedelta(days=30)
    from lms.models import Transaction
    collection = [ (Transaction.query.filter_by(user_id=user.user_id,
                        book_id=book.book_id).first(),book) for book in user.collection.all()]
    for trans,book in collection:
        transaction_time = trans.transaction_time.replace(tzinfo=timezone.utc)

        if cut_off<=transaction_time:
            book_content = {
                "book_name":book.book_name,
                "book_price":book.book_price,
                "rating":0
            }
            rating = Rating.query.filter_by(user_id=user.user_id,book_id=book.book_id).first()

            if rating:
                book_content['rating'] = rating.rating
            
            content['collection'].append(book_content)
            content['total_spending']+=book.book_price

    return content

def generate_pdf_from_html(html, output_path):
    from xhtml2pdf import pisa
    with open(output_path, "wb") as result_file:
        pisa_status = pisa.CreatePDF(html, dest=result_file)
    if pisa_status.err:
        print(f"Error generating PDF: {pisa_status.err}")



def delete_keys_matching(pattern):
    import redis,re
    redis_conn = redis.StrictRedis(host='localhost', port=6379, db=3)
    regex = re.compile(r".*{}.*".format(pattern))

    for key in redis_conn.scan_iter():
        decoded_key = key.decode('utf-8')
        if regex.match(decoded_key):
            redis_conn.delete(decoded_key)


def top_sellers():
    from lms import cache
    from lms.models import Book

    top_sell = cache.get('top_sellers')
    if top_sell:
        return top_sell
    else:

        sorted_books = sorted(Book.query.filter_by(is_available=True).all(),key=lambda x:x.vol_sold,reverse=True)  

        top_sell = sorted_books if len(sorted_books)<=7 else sorted_books[:7]

        top_sell = [book.book_id for book in top_sell]

        cache.set('top_sellers',top_sell,timeout= 24 * 60 * 60)

        return top_sell



def sections():
    from lms import cache
    from lms.models import Section

    sections = cache.get('sections')

    if sections:
        return sections
    else:

        sections = [section.to_json(type='BRIEF') for section in Section.query.filter(Section.section_name != 'DEFAULT').all()]
        cache.set('sections',sections,timeout= 6 * 60 * 60)

        return sections
    

def set_sections():
    from lms import cache
    from lms.models import Section


    sections = [section.to_json(type='BRIEF') for section in Section.query.filter(Section.section_name != 'DEFAULT').all()]
    cache.set('sections',sections,timeout= 6 * 60 * 60)

