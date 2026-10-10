import React from 'react';
import { StyleSheet, Text, View, SafeAreaView } from 'react-native';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.title}>Multi-Agents Mobile App</Text>
        <Text style={styles.subtitle}>Sản phẩm sinh tự động bởi AI Multi-Agent System</Text>
        <Text style={styles.status}>Backend Status: Connected (FastAPI)</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
    alignItems: 'center',
    justifyContent: 'center',
  },
  card: {
    padding: 24,
    borderRadius: 12,
    backgroundColor: '#1e293b',
    alignItems: 'center',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#38bdf8',
  },
  subtitle: {
    fontSize: 14,
    color: '#94a3b8',
    marginTop: 8,
  },
  status: {
    fontSize: 12,
    color: '#4ade80',
    marginTop: 16,
  },
});
