# OOP_mashq_1
Order Processing System — Qo‘llanma

Bu loyiha murakkab OOP strukturasini namoyish etadi va enterprise-level arxitekturaga yaqin yondashuvdan foydalanadi.

Asosiy tushunchalar:
1. Domain Layer

Order — biznes obyekt.

Status maydoni (CREATED → PAID) orqali jarayon boshqariladi.

2. Strategy Pattern

CardPayment va PaypalPayment — to‘lov strategiyalari.

PaymentStrategy abstract class orqali yagona interfeys yaratilgan.

Kengaytirish oson: yangi payment turi qo‘shish uchun faqat yangi sinf yoziladi.

3. Observer Pattern

LoggingListener va NotificationListener — event kuzatuvchilari.

OrderService ichidagi _notify() ularni ishga tushiradi.

Har safar order o‘zgarsa, barcha observerlarga xabar beriladi.

4. Repository Pattern

OrderRepository — abstrakt saqlash interfeysi.

InMemoryOrderRepository — real implementatsiya.

Xohlasang, keyin SqlOrderRepository yozishing mumkin — servis bunga bog‘liq emas.

5. OrderService

Domen jarayonlarini boshqaradi:

order yaratish

to‘lovni amalga oshirish

listeners’ni chaqirish

To‘liq loosе coupling va SOLID tamoyillariga mos.

6. Custom Exception

OrderException xatolarni boshqarish uchun ishlatiladi.
