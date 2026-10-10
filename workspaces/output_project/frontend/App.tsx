import React, {"useState", "useEffect"} from 'react';
import { SafeAreaView, View, Text, StyleSheet, FlatList, TouchableOpacity, Alert } from 'react-native';
import { SparePart, Appointment } from './types';

export default function App() {
  const [items, setItems] = useState<SparePart[]>([]);
  const [selectedSlot, setSelectedSlot] = useState<string>('2026-10-20T10:00:00Z');

  useEffect(() => {
    // Mock danh mục kết nối API Backend
    setItems([
      { id: 'item_001', name: 'Phụ tùng & Dịch vụ Sửa chữa Xe Tiêu chuẩn', price: 150000.0, stock_quantity: 50, is_active: true },
      { id: 'item_002', name: 'Phụ tùng & Dịch vụ Sửa chữa Xe Cao cấp', price: 225000.0, stock_quantity: 30, is_active: true }
    ]);
  }, []);

  const handleBooking = (item: SparePart) => {
    Alert.alert(
      'Xác nhận đặt đơn',
      `Bạn chọn ${item.name} vào khung giờ ${selectedSlot}. Đơn hàng tuân thủ quy tắc: Giới hạn tối đa 5 xe mỗi khung giờ (BR-01).`,
      [{ text: 'Hủy' }, { text: 'Đồng ý', onPress: () => Alert.alert('Thành công', 'Đã ghi nhận đơn!') }]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>EduMaster_App Mobile</Text>
        <Text style={styles.subtitle}>Phụ tùng & Dịch vụ Sửa chữa Xe</Text>
      </View>
      <FlatList
        data={items}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.itemName}>{item.name}</Text>
            <Text style={styles.itemPrice}>{item.price.toLocaleString('vi-VN')} VNĐ</Text>
            <TouchableOpacity style={styles.btn} onPress={() => handleBooking(item)}>
              <Text style={styles.btnText}>Đặt lịch ngay</Text>
            </TouchableOpacity>
          </View>
        )}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8FAFC', padding: 16 },
  header: { marginBottom: 20 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#0F172A' },
  subtitle: { fontSize: 14, color: '#64748B' },
  card: { backgroundColor: '#FFFFFF', padding: 16, borderRadius: 12, marginBottom: 12, elevation: 2 },
  itemName: { fontSize: 18, fontWeight: '600', color: '#1E293B' },
  itemPrice: { fontSize: 16, color: '#059669', marginVertical: 8, fontWeight: 'bold' },
  btn: { backgroundColor: '#0284C7', padding: 10, borderRadius: 8, alignItems: 'center' },
  btnText: { color: '#FFFFFF', fontWeight: 'bold' }
});
