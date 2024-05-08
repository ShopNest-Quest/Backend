const url = 'https://shopnest.pythonanywhere.com/seller/add_product?product_name=abc&price=85&description=ghdvgds&seller_username=sasi&category_id=2&stock=5&image_url=gdsbgh.jpg';

fetch(url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // Assuming response is JSON; you might need response.text() or other methods based on actual response type
  })
  .then(data => {
    console.log('Response:', data);
    // Handle the response data here
  })
  .catch(error => {
    console.error('Fetch error:', error);
    // Handle any errors that occurred during the fetch
  });
