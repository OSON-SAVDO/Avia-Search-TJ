import React, { useState, useEffect } from 'react';
import { StyleSheet, View, TextInput, Button, FlatList, Text, TouchableOpacity, ScrollView } from 'react-native';

const API_URL = 'http://localhost:3000/api';

export default function App() {
    const [search, setSearch] = useState({
        origin: '', destination: '', departDate: '', returnDate: '',
        adults: 1, children: 0, infants: 0
    });
    const [flights, setFlights] = useState([]);
    const [filteredFlights, setFilteredFlights] = useState([]);
    const [favorites, setFavorites] = useState([]);
    const [currency, setCurrency] = useState('USD');

    const handleSearch = async () => {
        const response = await fetch(`${API_URL}/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(search)
        });
        const data = await response.json();
        setFlights(data.data);
        setFilteredFlights(data.data);
    };

    const applyFilter = (type) => {
        let sorted = [...flights];
        if (type === 'cheap') sorted.sort((a, b) => a.value - b.value);
        if (type === 'direct') sorted = flights.filter(f => f.number_of_changes === 0);
        setFilteredFlights(sorted);
    };

    const toggleFavorite = (flight) => {
        setFavorites([...favorites, flight]);
    };

    return (
        <View style={styles.container}>
            <View style={styles.searchBox}>
                <TextInput placeholder="From" onChangeText={(v) => setSearch({...search, origin: v})} />
                <TextInput placeholder="To" onChangeText={(v) => setSearch({...search, destination: v})} />
                <TextInput placeholder="Date (YYYY-MM-DD)" onChangeText={(v) => setSearch({...search, departDate: v})} />
                <Button title="Search Flights" onPress={handleSearch} />
            </View>

            <View style={styles.filterRow}>
                <TouchableOpacity onPress={() => applyFilter('cheap')}><Text>Cheapest</Text></TouchableOpacity>
                <TouchableOpacity onPress={() => applyFilter('direct')}><Text>Non-stop</Text></TouchableOpacity>
            </View>

            <FlatList
                data={filteredFlights}
                keyExtractor={(item, index) => index.toString()}
                renderItem={({ item }) => (
                    <View style={styles.card}>
                        <Text style={styles.price}>{item.value} {currency}</Text>
                        <Text>{item.origin} ➔ {item.destination}</Text>
                        <Text>Stops: {item.number_of_changes}</Text>
                        <Button title="Favorite" onPress={() => toggleFavorite(item)} />
                        <Button title="Book Now" onPress={() => Linking.openURL(`https://www.aviasales.com${item.link}`)} />
                    </View>
                )}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, paddingTop: 50, paddingHorizontal: 20, backgroundColor: '#f5f5f5' },
    searchBox: { backgroundColor: '#fff', padding: 15, borderRadius: 10, elevation: 5 },
    filterRow: { flexDirection: 'row', justifyContent: 'space-around', marginVertical: 10 },
    card: { backgroundColor: '#fff', padding: 20, marginVertical: 8, borderRadius: 10 },
    price: { fontSize: 20, fontWeight: 'bold', color: '#2ecc71' }
});
