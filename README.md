# Online Auction Platform (Django)

A full-stack Django web application simulating an online auction marketplace. Users can create listings, place bids, comment on items, manage watchlists, and close auctions they own. No real transactions or payments are involved.

## Features

- User authentication (login, logout, registration)
- Create auction listings with title, description, category, image URL, and starting bid
- Place bids with server-side validation (bids must exceed current price)
- Automatic tracking of current highest bid
- Auction closure by listing creator with winner assignment
- Comment system on listings
- Watchlist functionality (add and remove listings)
- Browse active listings by category

## Tech Stack

- Backend: Python, Django
- Frontend: HTML, CSS
- Database: SQLite (via Django ORM)
- Authentication: Django built-in auth system

## Data Models

- User (Django auth user)
- Listing (auction item, creator, category, active status, winner)
- Bid (amount, bidder, listing)
- Comment (text, user, listing, timestamp)
- Watchlist (many-to-many relationship between users and listings)

## Permissions and Validation

- Only authenticated users can place bids or comments
- Only listing creators can close their auctions
- All bid validation is enforced server-side
- Authorization checks are handled in views, not templates

## Running Locally

```bash
git clone https://github.com/yourusername/auction-platform.git
cd auction-platform
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
