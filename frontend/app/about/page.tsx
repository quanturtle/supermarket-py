export default function AboutPage() {
	return (
	  <>
		<h1 className="text-3xl font-bold mb-6">About PriceTracker</h1>
  
		<div className="space-y-6 max-w-3xl bg-white p-6 rounded-lg shadow-sm mx-auto">
		  <p>
			PriceTracker is a service dedicated to helping consumers make informed purchasing decisions by providing
			transparent price comparisons across major supermarkets.
		  </p>
  
		  <h2 className="text-2xl font-semibold mt-8">Our Mission</h2>
		  <p>
			Our mission is to empower shoppers with the information they need to save money on everyday purchases. By
			tracking price histories and comparing current prices across multiple retailers, we help you find the best
			deals and understand pricing trends.
		  </p>
  
		  <h2 className="text-2xl font-semibold mt-8">How It Works</h2>
		  <p>
			PriceTracker collects pricing data from five major supermarkets on a daily basis. Our system processes this
			information to provide you with:
		  </p>
		  <ul className="list-disc pl-6 space-y-2 mt-2">
			<li>Current prices at each supermarket</li>
			<li>Price history charts showing how prices have changed over time</li>
			<li>Price change indicators showing recent price increases or decreases</li>
			<li>Information about which store currently offers the best price</li>
		  </ul>
  
		  <h2 className="text-2xl font-semibold mt-8">Our Team</h2>
		  <p>
			PriceTracker was founded in 2024 by a team of consumer advocates and data specialists who believe in price
			transparency. Our team works tirelessly to ensure the data we provide is accurate, up-to-date, and presented
			in a way that's easy to understand.
		  </p>
  
		  <h2 className="text-2xl font-semibold mt-8">Future Plans</h2>
		  <p>We're constantly working to improve PriceTracker. In the coming months, we plan to:</p>
		  <ul className="list-disc pl-6 space-y-2 mt-2">
			<li>Expand our coverage to include more supermarkets</li>
			<li>Add personalized price alerts for products you're interested in</li>
			<li>Develop a mobile app for on-the-go price checking</li>
			<li>Introduce price predictions based on historical trends</li>
		  </ul>
		</div>
	  </>
	)
  }