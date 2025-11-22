; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

@"true" = constant i1 1
@"false" = constant i1 0
define i32 @"main"()
{
main_entry:
  %".2" = alloca i32
  store i32 50, i32* %".2"
  %".4" = load i32, i32* %".2"
  %".5" = icmp eq i32 %".4", 19
  br i1 %".5", label %"main_entry.if", label %"main_entry.else"
main_entry.if:
  store i32 43, i32* %".2"
  br label %"main_entry.endif"
main_entry.else:
main_entry.endif:
  %".9" = load i32, i32* %".2"
  ret i32 %".9"
}
