import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    print(f"Corpus: {corpus}")
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    outbound_links = corpus[page]
    num_outbound_pages = len(outbound_links)
    num_corpus_pages = len(corpus.keys())
    model = {}
    for key in corpus.keys():
        model[key] = (1 - damping_factor) / num_corpus_pages
        if key in outbound_links:
            model[key] += damping_factor / num_outbound_pages
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages_visited = {}
    current_page = random.choice(list(corpus.keys()))
    for i in range(n):
        if current_page in pages_visited:
            pages_visited[current_page] += 1
        else:
            pages_visited[current_page] = 1

        next_page_transition_model = transition_model(corpus, current_page, damping_factor)

        weights = []
        for key in next_page_transition_model:
            weights.append(next_page_transition_model[key])

        # https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
        current_page = random.choices(list(next_page_transition_model.keys()), weights, k=1)[0]

    page_ranks = {}
    for key in pages_visited:
        page_ranks[key] = pages_visited[key] / n
    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    #  Start by assuming the PageRank of every page is 1 / N (i.e., equally likely to be on any page).
    num_corpus_pages = len(corpus.keys())
    page_ranks = {}
    for key in corpus.keys():
        page_ranks[key] = 1 / num_corpus_pages
    
    # Use the formula to calculate new PageRank values for each page, based on the previous PageRank values
    has_converged = False
    while not has_converged:
        has_converged = True

        # Keep repeating this process, calculating a new set of PageRank values for each page based on the previous set of PageRank values.
        for key in corpus.keys():
            sum_of_inbound_pagerank_values = 0
            for inbound_key in corpus.keys():
                if key in corpus[inbound_key]:
                    sum_of_inbound_pagerank_values += page_ranks[inbound_key] / len(corpus[inbound_key])
                    
            next_value = ((1.0 - damping_factor) / num_corpus_pages) + damping_factor * sum_of_inbound_pagerank_values

            # Eventually the PageRank values will converge (i.e., not change by more than a small threshold with each iteration).
            # This process should repeat until PageRank values converge.
            delta = abs(page_ranks[key] - next_value)
            if delta >= 0.0001:
                has_converged = False

            # Assign the new PageRank value
            page_ranks[key] = next_value
                
    return page_ranks




if __name__ == "__main__":
    main()
