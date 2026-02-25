# Code Templates Reference

## Table of Contents
1. [Freezed Models](#freezed)
2. [Repository Pattern](#repository)
3. [Navigation with GoRouter](#navigation)
4. [Form Handling](#forms)
5. [Responsive Layouts](#responsive)
6. [Custom Widgets](#widgets)
7. [Animations](#animations)
8. [Platform Channels](#platform-channels)
9. [Testing Templates](#testing)
10. [Localization](#l10n)

---

## Freezed Models {#freezed}

### Setup

```yaml
dependencies:
  freezed_annotation: ^2.4.1
  json_annotation: ^4.9.0

dev_dependencies:
  freezed: ^2.5.2
  json_serializable: ^6.8.0
  build_runner: ^2.4.8
```

### Model Template

```dart
// lib/features/products/data/models/product_model.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'product_model.freezed.dart';
part 'product_model.g.dart';

@freezed
class ProductModel with _$ProductModel {
  const factory ProductModel({
    required String id,
    required String name,
    required double price,
    @Default('') String description,
    @Default('uncategorized') String category,
    @JsonKey(name: 'image_url') String? imageUrl,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @Default(true) bool isActive,
  }) = _ProductModel;

  factory ProductModel.fromJson(Map<String, dynamic> json) =>
      _$ProductModelFromJson(json);
}

// Domain entity (pure, no annotations)
// lib/features/products/domain/entities/product.dart
class Product {
  final String id;
  final String name;
  final double price;
  final String description;
  final String category;
  final String? imageUrl;
  final DateTime? createdAt;
  final bool isActive;

  const Product({
    required this.id,
    required this.name,
    required this.price,
    this.description = '',
    this.category = 'uncategorized',
    this.imageUrl,
    this.createdAt,
    this.isActive = true,
  });
}

// Mapper extension
extension ProductModelX on ProductModel {
  Product toEntity() => Product(
    id: id, name: name, price: price, description: description,
    category: category, imageUrl: imageUrl, createdAt: createdAt,
    isActive: isActive,
  );
}

extension ProductX on Product {
  ProductModel toModel() => ProductModel(
    id: id, name: name, price: price, description: description,
    category: category, imageUrl: imageUrl, createdAt: createdAt,
    isActive: isActive,
  );
}
```

### Sealed Union for API Responses

```dart
@freezed
sealed class ApiResponse<T> with _$ApiResponse<T> {
  const factory ApiResponse.success(T data) = _Success<T>;
  const factory ApiResponse.error(String message, {int? code}) = _Error<T>;
  const factory ApiResponse.loading() = _Loading<T>;
}

// Usage
final response = ApiResponse<List<Product>>.success(products);
response.when(
  success: (data) => print('Got ${data.length} products'),
  error: (msg, code) => print('Error $code: $msg'),
  loading: () => print('Loading...'),
);
```

Build after creating models:
```bash
dart run build_runner build --delete-conflicting-outputs
```

---

## Repository Pattern {#repository}

```dart
// Domain (abstract contract)
abstract class ProductRepository {
  Future<List<Product>> getProducts({int page = 1, int limit = 20});
  Future<Product> getProduct(String id);
  Future<Product> addProduct(Product product);
  Future<Product> updateProduct(Product product);
  Future<void> deleteProduct(String id);
}

// Data (implementation)
class ProductRepositoryImpl implements ProductRepository {
  final ApiClient _apiClient;
  final ProductLocalSource _localSource;
  final NetworkInfo _networkInfo;

  ProductRepositoryImpl({
    required ApiClient apiClient,
    required ProductLocalSource localSource,
    required NetworkInfo networkInfo,
  }) : _apiClient = apiClient,
       _localSource = localSource,
       _networkInfo = networkInfo;

  @override
  Future<List<Product>> getProducts({int page = 1, int limit = 20}) async {
    if (await _networkInfo.isConnected) {
      try {
        final response = await _apiClient.get<List>(
          '/products',
          params: {'page': page, 'limit': limit},
        );
        final models = (response.data ?? [])
            .map((json) => ProductModel.fromJson(json as Map<String, dynamic>))
            .toList();
        await _localSource.cacheProducts(models);
        return models.map((m) => m.toEntity()).toList();
      } on DioException catch (e) {
        throw ServerException(
          e.message ?? 'Server error',
          statusCode: e.response?.statusCode,
        );
      }
    } else {
      final cached = await _localSource.getCachedProducts();
      if (cached.isNotEmpty) return cached.map((m) => m.toEntity()).toList();
      throw const NetworkException();
    }
  }

  @override
  Future<Product> getProduct(String id) async {
    final response = await _apiClient.get<Map<String, dynamic>>('/products/$id');
    return ProductModel.fromJson(response.data!).toEntity();
  }

  @override
  Future<Product> addProduct(Product product) async {
    final response = await _apiClient.post<Map<String, dynamic>>(
      '/products',
      data: product.toModel().toJson(),
    );
    return ProductModel.fromJson(response.data!).toEntity();
  }

  @override
  Future<Product> updateProduct(Product product) async {
    final response = await _apiClient.post<Map<String, dynamic>>(
      '/products/${product.id}',
      data: product.toModel().toJson(),
    );
    return ProductModel.fromJson(response.data!).toEntity();
  }

  @override
  Future<void> deleteProduct(String id) async {
    await _apiClient.get('/products/$id'); // or DELETE
  }
}

// Riverpod provider for the repository
@riverpod
ProductRepository productRepository(ProductRepositoryRef ref) {
  return ProductRepositoryImpl(
    apiClient: ref.read(apiClientProvider),
    localSource: ref.read(productLocalSourceProvider),
    networkInfo: ref.read(networkInfoProvider),
  );
}
```

---

## Navigation with GoRouter {#navigation}

### Full Router Setup with Auth Guard

```dart
// lib/routing/app_router.dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'app_router.g.dart';

@riverpod
GoRouter router(RouterRef ref) {
  final isAuth = ref.watch(isAuthenticatedProvider);

  return GoRouter(
    initialLocation: '/',
    debugLogDiagnostics: true,
    redirect: (context, state) {
      final loggingIn = state.matchedLocation == '/login';
      final registering = state.matchedLocation == '/register';

      if (!isAuth && !loggingIn && !registering) return '/login';
      if (isAuth && (loggingIn || registering)) return '/';
      return null;
    },
    routes: [
      // Auth routes (no shell)
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/register',
        builder: (context, state) => const RegisterScreen(),
      ),

      // Main app with bottom navigation shell
      StatefulShellRoute.indexedStack(
        builder: (context, state, shell) => MainShell(navigationShell: shell),
        branches: [
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/',
              builder: (context, state) => const HomeScreen(),
              routes: [
                GoRoute(
                  path: 'product/:id',
                  builder: (context, state) => ProductDetailScreen(
                    id: state.pathParameters['id']!,
                  ),
                ),
              ],
            ),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/search',
              builder: (context, state) => const SearchScreen(),
            ),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/profile',
              builder: (context, state) => const ProfileScreen(),
              routes: [
                GoRoute(
                  path: 'settings',
                  builder: (context, state) => const SettingsScreen(),
                ),
              ],
            ),
          ]),
        ],
      ),
    ],
    errorBuilder: (context, state) => ErrorScreen(error: state.error),
  );
}

// Shell with bottom nav
class MainShell extends StatelessWidget {
  final StatefulNavigationShell navigationShell;

  const MainShell({required this.navigationShell, super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: navigationShell,
      bottomNavigationBar: NavigationBar(
        selectedIndex: navigationShell.currentIndex,
        onDestinationSelected: (index) => navigationShell.goBranch(
          index,
          initialLocation: index == navigationShell.currentIndex,
        ),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.search), label: 'Search'),
          NavigationDestination(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}
```

### Deep Linking (Android)

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<intent-filter android:autoVerify="true">
  <action android:name="android.intent.action.VIEW"/>
  <category android:name="android.intent.category.DEFAULT"/>
  <category android:name="android.intent.category.BROWSABLE"/>
  <data android:scheme="https" android:host="example.com" android:pathPrefix="/product"/>
</intent-filter>
```

### Deep Linking (iOS)

```xml
<!-- ios/Runner/Info.plist — add inside <dict> -->
<key>FlutterDeepLinkingEnabled</key>
<true/>
```

And create `ios/Runner/Runner.entitlements`:
```xml
<dict>
  <key>com.apple.developer.associated-domains</key>
  <array>
    <string>applinks:example.com</string>
  </array>
</dict>
```

---

## Form Handling {#forms}

```dart
class LoginForm extends ConsumerStatefulWidget {
  const LoginForm({super.key});

  @override
  ConsumerState<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends ConsumerState<LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final formState = ref.watch(loginFormProvider);

    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          TextFormField(
            controller: _emailController,
            keyboardType: TextInputType.emailAddress,
            textInputAction: TextInputAction.next,
            autofillHints: const [AutofillHints.email],
            decoration: const InputDecoration(
              labelText: 'Email',
              prefixIcon: Icon(Icons.email_outlined),
            ),
            validator: (v) {
              if (v == null || v.isEmpty) return 'Email required';
              if (!v.isValidEmail) return 'Invalid email';
              return null;
            },
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _passwordController,
            obscureText: _obscurePassword,
            textInputAction: TextInputAction.done,
            autofillHints: const [AutofillHints.password],
            decoration: InputDecoration(
              labelText: 'Password',
              prefixIcon: const Icon(Icons.lock_outlined),
              suffixIcon: IconButton(
                icon: Icon(_obscurePassword ? Icons.visibility : Icons.visibility_off),
                onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
              ),
            ),
            validator: (v) {
              if (v == null || v.isEmpty) return 'Password required';
              if (v.length < 8) return 'Min 8 characters';
              return null;
            },
            onFieldSubmitted: (_) => _submit(),
          ),
          if (formState.error != null) ...[
            const SizedBox(height: 12),
            Text(formState.error!, style: TextStyle(color: context.colorScheme.error)),
          ],
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: formState.isSubmitting ? null : _submit,
            child: formState.isSubmitting
                ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2))
                : const Text('Login'),
          ),
        ],
      ),
    );
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    FocusScope.of(context).unfocus();

    final notifier = ref.read(loginFormProvider.notifier);
    notifier.updateEmail(_emailController.text.trim());
    notifier.updatePassword(_passwordController.text);

    final success = await notifier.submit();
    if (success && mounted) {
      context.go('/');
    }
  }
}
```

---

## Responsive Layouts {#responsive}

```dart
// lib/core/utils/responsive.dart
class Breakpoints {
  static const double mobile = 600;
  static const double tablet = 900;
  static const double desktop = 1200;
}

class ResponsiveLayout extends StatelessWidget {
  final Widget mobile;
  final Widget? tablet;
  final Widget? desktop;

  const ResponsiveLayout({
    required this.mobile,
    this.tablet,
    this.desktop,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(builder: (context, constraints) {
      if (constraints.maxWidth >= Breakpoints.desktop) {
        return desktop ?? tablet ?? mobile;
      }
      if (constraints.maxWidth >= Breakpoints.tablet) {
        return tablet ?? mobile;
      }
      return mobile;
    });
  }
}

// Usage
ResponsiveLayout(
  mobile: const ProductListMobile(),
  tablet: const ProductGridTablet(),
  desktop: const ProductDashboardDesktop(),
)
```

---

## Custom Widgets {#widgets}

### Shimmer Loading Placeholder

```dart
class ShimmerLoading extends StatefulWidget {
  final double width;
  final double height;
  final double borderRadius;

  const ShimmerLoading({
    this.width = double.infinity,
    this.height = 16,
    this.borderRadius = 8,
    super.key,
  });

  @override
  State<ShimmerLoading> createState() => _ShimmerLoadingState();
}

class _ShimmerLoadingState extends State<ShimmerLoading>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = context.isDark;
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Container(
          width: widget.width,
          height: widget.height,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(widget.borderRadius),
            gradient: LinearGradient(
              begin: Alignment(-1.0 + 2.0 * _controller.value, 0),
              end: Alignment(-1.0 + 2.0 * _controller.value + 1, 0),
              colors: isDark
                  ? [Colors.grey[800]!, Colors.grey[700]!, Colors.grey[800]!]
                  : [Colors.grey[300]!, Colors.grey[100]!, Colors.grey[300]!],
            ),
          ),
        );
      },
    );
  }
}
```

### Debounced Search Field

```dart
class DebouncedSearchField extends StatefulWidget {
  final ValueChanged<String> onChanged;
  final Duration debounceDuration;
  final String hintText;

  const DebouncedSearchField({
    required this.onChanged,
    this.debounceDuration = const Duration(milliseconds: 400),
    this.hintText = 'Search...',
    super.key,
  });

  @override
  State<DebouncedSearchField> createState() => _DebouncedSearchFieldState();
}

class _DebouncedSearchFieldState extends State<DebouncedSearchField> {
  Timer? _debounce;
  final _controller = TextEditingController();

  @override
  void dispose() {
    _debounce?.cancel();
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: _controller,
      decoration: InputDecoration(
        hintText: widget.hintText,
        prefixIcon: const Icon(Icons.search),
        suffixIcon: _controller.text.isNotEmpty
            ? IconButton(
                icon: const Icon(Icons.clear),
                onPressed: () {
                  _controller.clear();
                  widget.onChanged('');
                  setState(() {});
                },
              )
            : null,
      ),
      onChanged: (value) {
        setState(() {});
        _debounce?.cancel();
        _debounce = Timer(widget.debounceDuration, () => widget.onChanged(value));
      },
    );
  }
}
```

---

## Animations {#animations}

### Staggered List Animation

```dart
class StaggeredListItem extends StatelessWidget {
  final int index;
  final Widget child;

  const StaggeredListItem({required this.index, required this.child, super.key});

  @override
  Widget build(BuildContext context) {
    return TweenAnimationBuilder<double>(
      tween: Tween(begin: 0, end: 1),
      duration: Duration(milliseconds: 400 + (index * 100).clamp(0, 600)),
      curve: Curves.easeOutCubic,
      builder: (context, value, child) {
        return Opacity(
          opacity: value,
          child: Transform.translate(
            offset: Offset(0, 30 * (1 - value)),
            child: child,
          ),
        );
      },
      child: child,
    );
  }
}

// Usage in ListView.builder
itemBuilder: (context, index) => StaggeredListItem(
  index: index,
  child: ProductTile(product: products[index]),
),
```

---

## Testing Templates {#testing}

### Widget Test with Riverpod

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mocktail/mocktail.dart';

class MockProductRepository extends Mock implements ProductRepository {}

Widget createTestWidget(Widget child, {List<Override>? overrides}) {
  return ProviderScope(
    overrides: overrides ?? [],
    child: MaterialApp(home: child),
  );
}

void main() {
  group('ProductListScreen', () {
    late MockProductRepository mockRepo;

    setUp(() {
      mockRepo = MockProductRepository();
    });

    testWidgets('shows loading then data', (tester) async {
      when(() => mockRepo.getProducts())
          .thenAnswer((_) async => [
            const Product(id: '1', name: 'Widget', price: 9.99),
          ]);

      await tester.pumpWidget(createTestWidget(
        const ProductListScreen(),
        overrides: [
          productRepositoryProvider.overrideWithValue(mockRepo),
        ],
      ));

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      await tester.pumpAndSettle();
      expect(find.text('Widget'), findsOneWidget);
    });

    testWidgets('shows error and retry', (tester) async {
      when(() => mockRepo.getProducts()).thenThrow(Exception('Network error'));

      await tester.pumpWidget(createTestWidget(
        const ProductListScreen(),
        overrides: [
          productRepositoryProvider.overrideWithValue(mockRepo),
        ],
      ));

      await tester.pumpAndSettle();
      expect(find.text('Retry'), findsOneWidget);
    });
  });
}
```

### Integration Test

```dart
// integration_test/app_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('full login flow', (tester) async {
    app.main();
    await tester.pumpAndSettle();

    // Should see login screen
    expect(find.text('Login'), findsOneWidget);

    // Enter credentials
    await tester.enterText(find.byType(TextFormField).first, 'test@test.com');
    await tester.enterText(find.byType(TextFormField).last, 'password123');
    await tester.tap(find.text('Login'));
    await tester.pumpAndSettle(const Duration(seconds: 3));

    // Should navigate to home
    expect(find.text('Home'), findsOneWidget);
  });
}
```

---

## Localization {#l10n}

### Setup

```yaml
# pubspec.yaml
dependencies:
  flutter_localizations:
    sdk: flutter
  intl: ^0.19.0

flutter:
  generate: true
```

```yaml
# l10n.yaml
arb-dir: lib/core/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
```

```json
// lib/core/l10n/app_en.arb
{
  "@@locale": "en",
  "appTitle": "My App",
  "login": "Login",
  "email": "Email",
  "password": "Password",
  "itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}",
  "@itemCount": {
    "placeholders": { "count": { "type": "int" } }
  }
}
```

```json
// lib/core/l10n/app_ro.arb
{
  "@@locale": "ro",
  "appTitle": "Aplicația Mea",
  "login": "Autentificare",
  "email": "Email",
  "password": "Parola",
  "itemCount": "{count, plural, =0{Niciun element} =1{1 element} few{{count} elemente} other{{count} de elemente}}"
}
```

Usage: `AppLocalizations.of(context)!.login`

Generate with: `flutter gen-l10n`
