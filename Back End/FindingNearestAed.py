{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "ba8c2166-2aef-4270-94dc-56566494dc7e",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The quickest destination is: (51.24845, 4.4387075) (travel time: 1 hour 15 mins)\n"
     ]
    }
   ],
   "source": [
    "import googlemaps\n",
    "import points_within_circle from Getting GPS location.py\n",
    "import user_loc from Getting GPS location.py\n",
    "# Replace 'YOUR_API_KEY' with your actual API key\n",
    "#gmaps = googlemaps.Client(key='AIzaSyAvVZL_3CV1JvPsva1pO-lY5aMuWBvM1H4')\n",
    "\n",
    "# Define your starting location coordinates (latitude and longitude)\n",
    "start_location = user_loc\n",
    "\n",
    "# Define your list of destination points as coordinates (latitude and longitude)\n",
    "destinations = nearby_points\n",
    "\n",
    "# Calculate travel times to each destination\n",
    "travel_times = {}\n",
    "for destination in destinations:\n",
    "    directions = gmaps.directions(start_location, destination, mode=\"driving\")\n",
    "    if directions:\n",
    "        travel_time = directions[0]['legs'][0]['duration']['text']\n",
    "        travel_times[destination] = travel_time\n",
    "    else:\n",
    "        print(f\"No route found for destination: {destination}\")\n",
    "\n",
    "# Find the destination with the shortest travel time\n",
    "quickest_destination = min(travel_times, key=travel_times.get)\n",
    "print(f\"The quickest destination is: {quickest_destination} (travel time: {travel_times[quickest_destination]})\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
