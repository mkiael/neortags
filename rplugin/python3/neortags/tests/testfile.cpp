#include <iostream>
#include <vector>

class ITest
{
public:
   virtual ~ITest() {}

   virtual void print(const int value) const = 0;
};

class Test : public ITest
{
public:
   Test()
   {
   }

   void print(const int value) const
   {
      std::cout << "Value is: " << value << std::endl;
   }
};


int main()
{
   const Test test1;
   test1.print(1);

   Test test2;
   test2.print(2);

   return 0;
}
