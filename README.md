# Book-Heaven-PP5
![BookHeaven website preview](./assets/readme-images/responsive.PNG)

[Link to deployed site](https://book-heaven-e537b3f88787.herokuapp.com/)
Book Heaven is an online book shop, built using Python, Django, HTML, CSS, JavaScript, Amazon S3 and Stripe. 


# Table Of Content

-   [User Experience](#user-experience)
    -   [User Stories](#user-stories)
    -   [Site Goals](#site-goals)
    -   [Scope](#scope)
-   [Design](#design)
    -   [Colour Scheme](#colour-scheme)
    -   [Database Schema](#Database-Schema)
    -   [Fonts](#Fonts)
    -   [Wireframes](#Wireframes)
    -   [Agile Methodology](#Agile-Methodology)
         -   [Overview](#overview)
         -   [EPICS(Milestones)](#epicsmilestones)
         -   [User Stories issues](#user-stories-issues)
         -   [MoSCoW prioritization](#moscow-prioritization)
         -   [GitHub Projects](#github-projects)
-   [Features](#features)
    -   [Navbar](#Navbar)
    -   [Footer](#Footer)
    -   [Home](#Home)
        -   [Hero Section](#hero-section)
        -   [Search Form](#search-form)
        -   [Product Card](#product-card)
    -   [Profile Page](#profile-page)
    -   [Sign In Page](#sign-in-page)
    -   [Sign Up Page](#sign-up-page)
    -   [Sign Out Confirmation](#sign-out-confirmation)
    -   [Password reset](#password-reset)
    -   [Password reset email sent](#password-reset-email-sent)
    -   [Enter a new password](#enter-a-new-password)
    -   [Password Reset Completed](#password-reset-completed)
    -   [Error Pages](#error-pages)
-   [Future Features](#future-features)
-   [Marketing](#marketing)
-   [Search Engine Optimization SEO](#search-engine-optimization-seo)
-   [Testing](#testing)
-   [Bugs](#Bugs)
-   [Technologies And Languages](#technologies-and-languages)
    -   [Languages Used](#languages-used)
    -   [Python Modules](#python-modules)
    -   [Technologies and programs](#technologies-and-programs)
-   [Deployment](#deployment)
    -   [Before Deployment](#before-deployment)
    -   [Deployment on Heroku](#deployment-on-heroku)
    -   [Creating A Fork](#creating-a-fork)
    -   [Cloning Repository](#cloning-repository)
-   [Credits](#credits)
    -   [Media](#media)
    -   [Code](#code)
    -   [Acknowledgements](#acknowledgements)
    -   [Comments](#comments)


## User Experience

### User Stories
1. As a developer I can setup a new Django project so that I can create the project's structure
2. As a developer I can connect database and media storage so that the user's stored data is stored successfully
3. As a developer I can deploy the application early so that I can confirm that the initial setup is working and can continue testing the application during development
4. As a User I can navigate through the website so that I can access different sections efficiently
5. As a user I can visit the home page so that I can identify the purpose of the website
6. As a user I want to be able to view a list of all available products in the bookshop so that I can browse and choose books to purchase
7. As a user I want to be able to view detailed information about a single product so that I can make an informed decision before purchasing
8. As a user I want to be able to refine the list of available products by selecting a specific category so that I can easily find books that match my interests
9. As a User I want to be able to view detailed information about a product's author, including their name, a short biography, and a list of books available for sale on the website so that I can learn more about the author and explore their other works.
10. As a User I want to be able to search for products in the bookshop by entering keywords so that I can quickly find specific books or topics of interest
11. As a User I want to be able to browse through a large list of products in the bookshop so that I can view all books in an organised way
12. As a an authenticated user I want to be able to add a review for a book product so that I can share my feedback and experiences with other potential buyers
13. As a user I want to be able to register an account so that I can have access to all functionality of BookHeaven.
14. As a user, I want to be able to log in to my account so that I can access my personalized features and make purchases on BookHeaven.
15. As a registered user I want to be able to reset my password so that I can regain access to my account in case I forget my password
16. As a registered user I want to be able to see my profile page so that I can update my information
17. As a authenticated user, I want to be able to save books to my wishlist so that I can revisit and consider purchasing them later on BookHeaven.
18. As a user, I want to be able to add products to my shopping cart so that I can conveniently review and purchase multiple items at once on BookHeaven.
19. As a user, I want to be able to remove products from my shopping cart so that I can adjust my order before making a purchase on BookHeaven.
20. As a user, I want to be able to adjust the quantity of products in my shopping cart so that I can control the quantity of items I want to purchase on BookHeaven.
21. As a user, I want to be able to apply discount codes to my orders so that I can enjoy savings and discounts on my purchases at BookHeaven.
22. As a user, I want to be able to securely make payments using Stripe so that I can complete my purchases on BookHeaven with confidence.
23. As an administrator, I want to have access to an admin dashboard so that I can monitor and view simple statistics related to the orders made on BookHeaven.
24. As an administrator, I want to be able to add new products to the website so that I can expand the product catalog on BookHeaven.
25. As an administrator, I want to be able to remove products from the website so that I can manage the product catalog on BookHeaven.
26. As an administrator, I want to be able to edit existing products on the website so that I can update and manage the product catalog on BookHeaven.
27. As an administrator, I want to be able to edit the stock levels of products so that I can manage inventory and ensure product availability on BookHeaven.
28. As a user, I want to be able to submit a testimonial about my overall experience with the website so that I can provide feedback and share my positive experiences on BookHeaven.
29. As a user, I want to be able to view testimonials submitted by other users so that I can read about the experiences and feedback of fellow users on BookHeaven.
30. As a website owner, I want to improve the website's search engine optimization (SEO) so that the website can rank higher in search engine results and attract more organic traffic.
31. As a user, I want to sign up for newsletters on the website so that I can keep up with updates and deals.
32. As a user I want to be able to sort the list of available products by name and price so that I can easily find books that match my interests
33. As a User I want to be able to complete the checkout process for my shopping cart so that I can purchase the items I've added to my cart
34. As a an authenticated user I want to be able to delete my reviews for a book product so that I can manage and maintain the accuracy and relevance of my feedback
35. As a an authenticated user I want to be able to edit my reviews for a book product so that I can manage and maintain the accuracy and relevance of my feedback

### Site Goals
1. To provide users with a place to purchase books of their interest.
2. To provide the users the ability to search and browse books and authors.
3. To provide the users with the ability to save books to their wishlist
4. To provide the users with the ability to check their order history.
5. To provide the users with the most recents titles on the market.
6. To provide the users with the ability to leave a feedback for books they have purchased.

### Scope
The project aims to develop an e-commerce website offering books to customers. The website will be responsive and user-friendly, providing the user with the ability to:
 - Register and Login
 - Reset Password
 - Browse, search and refine books for sale
 - Add books to shopping cart
 - Apply discount codes
 - View product stock levels
 - Update quantity in shopping cart
 - Delete items from shopping cart
 - Pay for items securely by using the integrated Stripe payment system
 - Save books to wishlist
 - Update personal information
 - View past orders

Key Features:

1. Initial Project Setup:
- Developers can set up a new Django project to create the project's structure.
- Database and media storage will be connected to ensure data storage and retrieval.
- An early deployment of the application will be carried out to confirm the initial setup's functionality.
2. Products:
- Users can view books for sale and refine them by category and genre
- Users can sort products by price, title, genre or category
- Users can view details about each product including image, description, author, stock level and reviews
- Search products by title, author or description
- Registered users can leave reviews.
3. User Authentication:
- Users can register an account, allowing them access to all of the website's functionality.
- Registered users can login and access wishlist, reviews, past orders and saving personal details.
- Users can reset their password
- Users can add or remove items from their wishlist
4. Orders and checkout:
- Users can add items to their shopping cart
- Users can update the quantity of the items in the shopping cart
- Users can remove products from their shoppingcart
- Users can apply discount codes
- Users can use secure checkout functionality to pay for their items
5. Admin functionality:
The functionality in this section is limited to superusers or admins.
- Admins can access the admin dashboard, containing of a list of products and summary of orders and revenue.
- Admins can add products (books) for sale.
- Admins can delete products from the system.
- Admins can edit products and stock levels.
- Admins can access Orders section, where the order status can be updated.
- Admins can sort orders by status (In Progress, Completed, Cancelled)
- Admins can access the discount codes page, where codes can be created, deactivated or deleted.
6. Notification Messages:
Users will receive notification messages when performing CRUD operations, login/logout, and signup actions.

Benefits:

1. User-Centric Experience: The platform focuses on the user's needs, allowing efficient browsing and product purchasing.
2. Efficient Navigation: Users can easily navigate through different sections of the website for seamless access.
4. Effective Communication: Sending emails and notification messages features, enhances user interaction.

## Design
### Colour Scheme
The website harmoniously blends warm tones of light coral and red-orange with accents of light grey and white, all anchored by a cool grey undertone. This carefully curated color scheme establishes a sense of vibrancy and professionalism while ensuring a visually engaging experience for the users.
![Colour Schema](./assets/readme-images/colour-schema.PNG)
### Database Schema
