import java.util.ArrayList;
import java.util.List;

public class ListTests {
    @SuppressWarnings("unused")
    public static void main(String[] args) {
        /*
         * preamble
         * - [n]
         *     I will use [n] to cite sources, use the find text feature to find it.
         * - "default"
         *     I use default to mean package-private
         * - "nested class"
         *     "any class whose declaration occurs within the body of another class or interface declaration."[3]
         * - "inner class"
         *      "An inner class is a nested class that is not explicitly or implicitly static."[3]
         * 
         * <<<<<<TL;DR>>>>>>
         * copied from https://docs.oracle.com/javase/tutorial/java/javaOO/whentouse.html
         * Nested class:
         * - Use it if your requirements are similar to those of a local class, you
         *   want to make the type more widely available, and you don't require
         *   access to local variables or method parameters.
         * - Use a non-static nested class (or inner class) if you require access to
         *   an enclosing instance's non-public fields and methods. Use a static
         *   nested class if you don't require this access.
         * <<<<<<TL;DR>>>>>>
         */
        
        // we dont constraint to interface type yet
        // so we can view class specific behaviors
        ListPrivateStatic<Integer> listPrivateStatic = new ListPrivateStatic<>();
        ListDefaultStatic<Integer> listDefaultStatic = new ListDefaultStatic<>();
        ListPrivateNonStatic<Integer> listPrivateNonStatic = new ListPrivateNonStatic<>();
        ListDefaultNonStatic<Integer> listDefaultNonStatic = new ListDefaultNonStatic<>();

        List<TestList<Integer>> testLists = new ArrayList<>();

        // bundle the lists up so it's easier to work with
        testLists.add(listPrivateStatic);
        testLists.add(listDefaultStatic);
        testLists.add(listPrivateNonStatic);
        testLists.add(listDefaultNonStatic);

        // add 0, 1, 2, 3, 4 to every list
        for (int i = 0; i < 5; i++) {
            for (var l : testLists) {
                l.add(i);
            }
        }

        // print every list
        for (var l : testLists) {
            System.out.println(l.getKind());
            l.print();
            System.out.print("\n\n");
        }

        // every list up to now behaves the same
        // for both add and print

        /*
         * In the below section, we will test instantiating the
         * nested Node class from each of our list implementations.
         * 
         * We will try to instantiate it two ways:
         * 1. instantiate like a top level class
         * 2. instantiate with respect to a specific instance of
         *    the outer class
         * 
         * This will help us build understanding on the two types
         * of modifers going here
         * 
         * private vs default (blank)
         * static vs non-static (blank)
         * 
         * NOTE:
         * we used private vs default as the comparison mode here,
         * which is no issue since our driver is in the same package
         * as the list implementations. this behavior can be 
         * extrapolated to other access behaviors through other
         * access modifiers vs private.
         */

        /*
         * PRIVATE STATIC
         * neither instantiations will work
         * 
         * ListPrivateStatic<Integer>.Node nPS1 = new ListPrivateStatic<>.Node(10);
         * 
         * > the syntax is correct, however ListPrivateStatic.Node
         * > is in scope and will fail to compile
         * 
         * ListPrivateStatic<Integer>.Node nPS2 = listPrivateStatic.new Node<>(10);
         * 
         * > the syntax is wrong. even if you were to change the
         * > access modifier from private to default/public, the
         * > compilation will fail.
         */

        // ListPrivateStatic<Integer>.Node nPS1 = new ListPrivateStatic<>.Node(10);
        // ListPrivateStatic<Integer>.Node nPS2 = listPrivateStatic.new Node<>(10);


        /* 
         * DEFAULT STATIC
         * our nested class is static here, it does not bind to
         * any specific instance of the outer class through
         * implicit references, thus we declare it like a top 
         * level class
         * 
         * ListDefaultStatic.Node<Integer> nDS1 = new ListDefaultStatic.Node<>(10);
         * 
         * > this will be a valid statemnt
         * 
         * ListDefaultStatic.Node<Integer> nDS2 = listDefaultStatic.new Node<>(10);
         * 
         * > this is invalid syntax
         * > OuterInstance.new Inner() only applies
         * > to inner (non-static) classes
         * 
         */

        ListDefaultStatic.Node<Integer> nDS1 = new ListDefaultStatic.Node<>(10);
        // ListDefaultStatic.Node<Integer> nDS2 = listDefaultStatic.new Node<>(10);
        
        /*
         * PRIVATE NON-STATIC
         * 
         * neither instantions will work because of visibility
         * issues. this is similar to the PRIVATE STATIC case,
         * where even if you used the correct syntax, the private
         * modifier prevents us from seeing it.
         */

        // ListPrivateNonStatic<Integer>.Node nPNS1 = new ListPrivateNonStatic<>.Node(10);
        // ListPrivateNonStatic<Integer>.Node nPNS2 = listPrivateNonStatic.new Node(10);

        /* 
         * DEFAULT NON-STATIC
         * 
         * since our nested class is non-static here, it must contain
         * an implicit reference to an instance of the outer class.
         * thus we have to instantiate with respect to a specific
         * outer class instance.
         */

        // ListDefaultNonStatic<Integer>.Node nDNS1 = new ListDefaultNonStatic<>.Node(10);
        ListDefaultNonStatic<Integer>.Node nDNS2 = listDefaultNonStatic.new Node(10);

        /*
         * ===IMPORTANT===
         * I am not familiar with modern java design principles and 
         * might have an outdated view on the design aspect of Java.
         * Many behaviors in java exist because of backwards compatibility,
         * and might not be best-practice nowadays.
         * 
         * I highly recommend reading Oracle's Nested class documentation[2]
         * alongside this file, linked below.
         * ===============
         * 
         * ====================================================
         * ACCESS MODIFIERS
         * ----------------
         * 
         * So we notice something, our nested class being static or 
         * not does not affect the ability for a class with a certain
         * scope to instantiate it, it simply forces us to have an
         * instance of the outer class.
         * 
         * This brings us to a question, why have static nested classes
         * at all, since it basically functions like a top-level class?
         * Couldn't we just have "class Node" on the top level and make
         * it accessible only from the same package?
         * 
         * Not quite. It is a possible implementation, but if we wanted our
         * nested class to ONLY be accessible from the class outside of it,
         * then we would have to make it a private nested class.
         * 
         * Then comes the other question, okay so why do we allow public
         * static nested classes then? Surely we could just do the same
         * thing with normal public top-level classes?
         * 
         * Again, not quite. Functionally, we could do the same thing
         * with public top-level classes. However, static nested classes
         * allow us to be more expressive with our design intentions.
         * 
         * When we create a public static nested class, we're saying 
         * "Yes, you can create this nested class without a specific
         * INSTANCE of the outerclass. However, in my design, this nested
         * class is only meaningful in the context of the outer class."
         * 
         * 
         * For example, in this HttpRequest class,
         * 
         * public class HttpRequest {
         *     public static class Builder {
         *         ...
         *     }
         * }
         * 
         * 
         * Then when trying to build a request, we'd call,
         * 
         * HttpRequest request = new HttpRequest.Builder()
         *     .url(...)
         *     ...
         * 
         * Our builder isn't tied to any specific requests, but it's 
         * logically "owned" by the HttpRequest class, this builder
         * would make no sense elsewhere.
         * 
         * ====================================================
         * STATIC vs NON-STATIC
         * --------------------
         * 
         * Let's look at our specific linked list example to think
         * about static vs non-static.
         * 
         * The effective core difference between a static and non-static
         * class is that the non-static nested class has an implicit 
         * reference (check footnote for detail) a specific outer class
         * instance. Semantically, the non-static class is "bound" to 
         * some specific outer class.
         * 
         * So in our list example, when we create a non-static node,
         * 
         * ListDefaultNonStatic<Integer>.Node nDNS2 =
         *     listDefaultNonStatic.new Node(10);
         * 
         * This node we just created is semantically bound to the 
         * listDefaultNonStatic object.
         * 
         * The static version is as such,
         * 
         * ListDefaultStatic.Node<Integer> nDS1 =
         *     new ListDefaultStatic.Node<Integer>(10);
         * 
         * Notice how there's no reference of any outer object, we simply
         * refer to the top level type ListDefaultStatic.Node parmeterized
         * by <Integer>.
         * 
         * Functionally, through our simple number adding and printing
         * earlier, we can see that these two node types produce the same
         * behavior when in a linked list. The difference is the intention
         * of our design (and the implicit reference).
         * 
         * Let's look at our linked list implementation.
         * 
         *  myList.head
         *          |
         *          v
         *      [Node1] -> [Node2] -> [Node3] -> [Node4] -> [Node5]
         * 
         * Our linked list only contains a reference to some Node object 
         * that we take to represent the "head" of the list. The actual
         * structure of this linked list is induced by the Node class 
         * itself, not our linked list. Node has a ".next" field which
         * references the next node, creating a chain of sorts.
         * 
         * Thus, our linked list more precisely:
         * 
         * "represents the start of a list, where the whole list is
         *  induced by following the chain of nodes."
         * 
         * So the question of static vs non-static comes down to:
         * 
         * - "Are instances of specifically related to a particular
         *    instance of a list?"
         * - "Does our node perhaps store meta information about the
         *    list whose chain it belongs to?"
         * - "Do our nodes only ever 'belong' to one head node?"
         * 
         * ====================================================
         * WHEN DO WE USE EACH CASE?
         * -------------------------
         * 
         * So what are some use cases for each of these nested class
         * implementations? (I will use public vs private here.)
         * 
         * > private static
         * We don't want other classes to directly instantiate our Node
         * classes, they should only be able to interact with the Node
         * through methods we provide. Our node also has no semantic
         * relation any specific  List we implement, it only knows the
         * data it holds, and which nodes comes next.
         * 
         * > private non-static
         * We don't want other classes to directly instantiate our Node
         * classes, they should only be able to interact with the Node
         * through methods we provide. However, out node is related to a
         * specific list instance. Maybe we want to store information about
         * the length of the list that points to the head of some chain
         * it is part of, and NO other lists can hold references to any
         * part of the chain. Then we would have a non-static nested class
         * so we can have some member int length, keeping track of total
         * length.
         * 
         * > public static
         * Other classes can instantiate our nested class directly. The
         * HttpRequest and Builder example has this. The builder isn't
         * related to any specific HttpRequest, but this Building is
         * only meaningful in the context of HttpRequest.
         * 
         * > public non-static
         * Imagine a Button object that has an EventListener. You might 
         * want to pass this Listener around for other logic, but it 
         * has to be tightly coupled with a button instnace, as a Listener
         * on its own might make no sense at all.
         * 
         * For a simple singly linked list that we tried to create, we 
         * would prefer "private static class Node<E>". There's no coupling
         * to some particular outer instance, we don't need the implicit
         * reference. The class is also properly encapsulated through
         * the private modifier.
         * 
         * =================================================
         * FUN EXAMPLE
         * -----------
         * 
         * Here is a fun example of a complex node structure that could
         * be modelling something which we'd use non-static nodes for.
         * 
         *        anotherList.head -> [Node7]
         *                               |
         *                               V
         *  myList.head               [Node6]
         *          |                    |
         *          v                    v
         *      [Node1] -> [Node2] -> [Node3] -> [Node4] -> [Node5]
         *                               ^
         *                               |
         *                   otherList.head
         * 
         * myList      := [Node1] -> [Node2] -> [Node3] -> [Node4] -> [Node5]
         * otherList   := [Node3] -> [Node4] -> [Node5]
         * anotherList := [Node6] -> [Node7] -> [Node3] -> [Node4] -> [Node5]
         * 
         * This could however be considered bad design, since we don't
         * have a large object containing the entire structure of the
         * node chain.
         * 
         * =========================================================
         * FOOTNOTE
         * --------
         * 
         * The implicit reference means there's a field in our nested class
         * object that references the outer class object, that's how we can
         * access outer class members and methods.
         * 
         * In oracle's JDK18 release notes[1], they state that:
         * 
         * "Prior to JDK 18, when javac compiles an nested class
         *  it always generates a private synthetic field with a
         *  name starting with this$ to hold a reference to the
         *  enclosing instance, even if the nested class does not
         *  reference its enclosing instance and the field is unused.
         *  Starting in JDK 18, unused this$ fields are omitted;
         *  the field is only generated for nested classes that
         *  reference their enclosing instance."
         * 
         * 
         * If my understanding is right, this means if your nested
         * class does not reference the the outer class in anyway,
         * through direct references, member variables, or methods,
         * then javac will not generate this implicit reference,
         * which will allow for the garbage collector to clean up
         * the outer object earlier. This alleviates an issue that
         * used to occur. If you had nested classes referencing
         * massive outer classes, you keep reference to the nested
         * class but let the outer class go out of scope, your
         * nested class' implicit reference will keep the outer 
         * class alive, preventing GC from cleaning it up. This 
         * can result in unexpected amounts of memory build-up.
         * 
         * 
         * [1] https://www.oracle.com/java/technologies/javase/18-relnote-issues.html
         * [2] https://docs.oracle.com/javase/tutorial/java/javaOO/nested.html
         * [3] https://docs.oracle.com/javase/specs/jls/se25/html/jls-8.html
         */
    }
}

interface TestList<T> {
    public void add(T t);
    public void print();
    public String getKind();
}


class ListPrivateStatic<T> implements TestList<T> {
    private static class Node<E> { // use E here to prevent generic type param shadowing
        E data;
        Node<E> next;
        Node(E data) { this.data = data; }
    }

    private Node<T> head;

    public void add(T t) {
        if (head == null) {
            head = new Node<>(t);
        } else {
            Node<T> cur = head;
        
            while (cur.next != null) {
                cur = cur.next;
            }

            cur.next = new Node<>(t);
        }
    }

    public void print() {
        Node<T> cur = head;

        if (cur == null) {
            return;
        }

        System.out.print(cur.data);

        while (cur.next != null) {
            cur = cur.next;
            System.out.print(" -> " + cur.data);
        }
    }

    public String getKind() {
        return "private static";
    }
}

class ListDefaultStatic<T> implements TestList<T>{
    static class Node<E> {
        E data;
        Node<E> next;
        Node(E data) { this.data = data; }
    }

    private Node<T> head;

    public void add(T t) {
        if (head == null) {
            head = new Node<>(t);
        } else {
            Node<T> cur = head;
        
            while (cur.next != null) {
                cur = cur.next;
            }

            cur.next = new Node<>(t);
        }
    }

    public void print() {
        Node<T> cur = head;

        if (cur == null) {
            return;
        }

        System.out.print(cur.data);

        while (cur.next != null) {
            cur = cur.next;
            System.out.print(" -> " + cur.data);
        }
    }

    public String getKind() {
        return "default static";
    }
}

class ListPrivateNonStatic<T> implements TestList<T>{
    /*
     * notice how we don't need to declare generic here
     * since Node is not static here, it will always be
     * tied" to an instance of the outer class, thus the
     * nested class can directly use the generic declaration
     * of the outer class.
     * 
     * static class requires a declaration as they function
     * like top-level classes, which means they can be
     * instantiated by themselves without an instance of 
     * the outer class.
     */
    
    private class Node {
        T data;
        Node next;
        Node(T data) { this.data = data; }
    }

    private Node head;

    public void add(T t) {
        if (head == null) {
            head = new Node(t);
        } else {
            Node cur = head;
        
            while (cur.next != null) {
                cur = cur.next;
            }

            cur.next = new Node(t);
        }
    }

    public void print() {
        Node cur = head;

        if (cur == null) {
            return;
        }

        System.out.print(cur.data);

        while (cur.next != null) {
            cur = cur.next;
            System.out.print(" -> " + cur.data);
        }
    }

    public String getKind() {
        return "private non-static";
    }
}

class ListDefaultNonStatic<T> implements TestList<T>{
    /*
     * notice how we don't need to declare generic here
     * since Node is not static here, it will always be
     * tied" to an instance of the outer class, thus the
     * nested class can directly use the generic declaration
     * of the outer class.
     * 
     * static class requires a declaration as they function
     * like top-level classes, which means they can be
     * instantiated by themselves without an instance of 
     * the outer class.
     */
    
    class Node {
        T data;
        Node next;
        Node(T data) { this.data = data; }
    }

    private Node head;

    public void add(T t) {
        if (head == null) {
            head = new Node(t);
        } else {
            Node cur = head;
        
            while (cur.next != null) {
                cur = cur.next;
            }

            cur.next = new Node(t);
        }
    }

    public void print() {
        Node cur = head;

        if (cur == null) {
            return;
        }

        System.out.print(cur.data);

        while (cur.next != null) {
            cur = cur.next;
            System.out.print(" -> " + cur.data);
        }
    }

    public String getKind() {
        return "default non-static";
    }
}

class TestClass{
    @SuppressWarnings("unused")
    public static void test() {
        ListPrivateNonStatic<Integer> l1 = new ListPrivateNonStatic<>();
        // ListPrivateNonStatic<Integer>.Node node = l1.new Node(10); // node is private, not in scope even in same file

        ListDefaultNonStatic<Integer> l2 = new ListDefaultNonStatic<>();
        ListDefaultNonStatic<Integer>.Node node = l2.new Node(10);
    }
}