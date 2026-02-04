import React, { useState } from 'react';
import { StyleSheet, View, TextInput, Button, FlatList, Text, Linking, ScrollView } from 'react-native';

export default function App() {
  const [origin, setOrigin] = useState('DYU');
  const [destination, setDestination] = useState('MOW');
  const [departDate, setDepartDate] = useState('2024-12-01');
  const [flights, setFlights] = useState([]);

  const API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'; // ТОКЕНИ ХУДРО ИНҶО МОНЕД
  const MARKER = '701004';       // МАРКЕРИ ХУДРО ИНҶО МОНЕД

  const searchFlights = async () => {
    const url = `https://api.travelpayouts.com/v2/prices/latest?origin=${origin}&destination=${destination}&beginning_of_period=${departDate}&token=${API_TOKEN}&currency=usd`;
    
    try {
      const response = await fetch(url);
      const data = await response.json();
      if (data.success) {
        setFlights(data.data);
      } else {
        alert("Чипта ёфт нашуд");
      }
    } catch (error) {
      alert("Хатогии пайвастшавӣ ба API");
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>AVIA-SEARCH APP</Text>
      
      <View style={styles.searchBox}>
        <TextInput style={styles.input} placeholder="Аз куҷо (DYU)" onChangeText={setOrigin} value={origin} />
        <TextInput style={styles.input} placeholder="Ба куҷо (MOW)" onChangeText={setDestination} value={destination} />
        <TextInput style={styles.input} placeholder="Сана (YYYY-MM-DD)" onChangeText={setDepartDate} value={departDate} />
        <Button title="Ҷустуҷӯ" onPress={searchFlights} color="#ff6d00" />
      </View>

      {flights.map((item, index) => (
        <View key={index} style={styles.card}>
          <Text style={styles.price}>${item.value}</Text>
          <Text>{item.origin} ➔ {item.destination}</Text>
          <Text>Сана: {item.depart_date}</Text>
          <Button 
            title="ХАРИДАН" 
            onPress={() => Linking.openURL(`https://www.aviasales.tj/search/${item.origin}${item.depart_date}${item.destination}1?marker=${MARKER}`)} 
          />
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#f0f4f7' },
  title: { fontSize: 24, fontWeight: 'bold', textAlign: 'center', marginVertical: 20, color: '#007bff' },
  searchBox: { backgroundColor: '#fff', padding: 15, borderRadius: 10, marginBottom: 20 },
  input: { borderBottomWidth: 1, marginBottom: 15, padding: 8 },
  card: { backgroundColor: '#fff', padding: 15, borderRadius: 10, marginBottom: 15, borderLeftWidth: 5, borderLeftColor: '#007bff' },
  price: { fontSize: 22, fontWeight: 'bold', color: '#28a745' }
});
