import React from 'react';
import { SafeAreaView, Text, View, StyleSheet } from 'react-native';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.title}>HealthClinicApp</Text>
        <Text style={styles.subtitle}>Phát triển bởi Google Antigravity SDK Multi-Agents</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#F8FAFC' },
  card: { padding: 24, borderRadius: 16, backgroundColor: '#FFFFFF', elevation: 4 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#1E293B', marginBottom: 8 },
  subtitle: { fontSize: 14, color: '#64748B' }
});
