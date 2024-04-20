import std/json
import marshal
import tables

type
  F_VI = proc(): int
  F_SS = proc(arg: string): string
  F_SI = proc(arg: string): int
  F_II = proc(arg: int): int
  F_FF = proc(arg: float): float
  F_JJ = proc(arg: JsonNode): JsonNode

  Row = object
    name: string
    n: int

var RUN_MAP = initTable[string, int]()

var F_VI_TAB = newSeq[F_VI]()
var F_SS_TAB = newSeq[F_SS]()
var F_SI_TAB = newSeq[F_SI]()
var F_II_TAB = newSeq[F_II]()
var F_FF_TAB = newSeq[F_FF]()
var F_JJ_TAB = newSeq[F_JJ]()

proc register_python_fun*(fun: F_VI, name: string) =
  RUN_MAP[name & ":vi"] = F_VI_TAB.len
  F_VI_TAB.add(fun)

proc register_python_fun*(fun: F_SS, name: string) =
  RUN_MAP[name & ":ss"] = F_SS_TAB.len
  F_SS_TAB.add(fun)

proc register_python_fun*(fun: F_SI, name: string) =
  RUN_MAP[name & ":si"]=F_SI_TAB.len
  F_SI_TAB.add(fun)

proc register_python_fun*(fun: F_II, name: string) =
  RUN_MAP[name & ":ii"]=F_II_TAB.len
  F_II_TAB.add(fun)

proc register_python_fun*(fun: F_FF, name: string) =
  RUN_MAP[name & ":ff"]=F_FF_TAB.len
  F_FF_TAB.add(fun)

proc register_python_fun*(fun: F_JJ, name: string) =
  RUN_MAP[name & ":jj"]=F_JJ_TAB.len
  F_JJ_TAB.add(fun)

proc NimMain() {.cdecl, importc.}

proc library_init(): cstring {.exportc, dynlib, cdecl.} =
  NimMain()
  var buf = newSeq[Row]()
  for key, val in RUN_MAP:
    buf.add(Row(name:key, n:val))
  return ($$buf).cstring

proc fun_vi(fun_id: cint): cint {.exportc, dynlib, cdecl.} = 
  return F_VI_TAB[fun_id]().cint

proc fun_ss(fun_id: cint, arg: cstring): cstring {.exportc, dynlib, cdecl.} = 
  let ret = F_SS_TAB[fun_id]($arg)
  return ret.cstring

proc fun_si(fun_id: cint, arg: cstring): cint {.exportc, dynlib, cdecl.} = 
  return F_SI_TAB[fun_id]($arg).cint

proc fun_ii(fun_id: cint, arg: cint): cint {.exportc, dynlib, cdecl.} = 
  return F_II_TAB[fun_id](arg).cint

proc fun_ff(fun_id: cint, arg: cdouble): cdouble {.exportc, dynlib, cdecl.} = 
  var ret = F_FF_TAB[fun_id](arg)
  return ret

proc fun_jj(fun_id: cint, arg: cstring): cstring {.exportc, dynlib, cdecl.} =
  let ret =  F_JJ_TAB[fun_id](parseJson($arg))
  return ($ret).cstring

proc library_deinit() {.exportc, dynlib, cdecl.} =
  echo "Nothing to do here since we don't have any global memory"
  GC_FullCollect()
